#!/usr/bin/env python3
"""Schedule an approved day's posts in Buffer.

- Respects config/settings.json (publishing_enabled, dry_run).
- Idempotent: posts already in data/published.json are skipped.
- Media must already be live on GitHub Pages (checked with retries).
- Appends every scheduled post to data/posts.jsonl (the log the analyst and editor read).

Usage: python scripts/publish_buffer.py 2026-11-23
"""
import json, os, sys, time, urllib.request
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from buffer import gql, BufferError
from validate_plan import validate

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CREATE = """mutation($input: CreatePostInput!) {
  createPost(input: $input) {
    ... on PostActionSuccess { post { id dueAt status } }
    ... on MutationError { message }
  }
}"""


def jload(path, default):
    return json.load(open(path)) if os.path.exists(path) else default


def url_live(url, tries=12, wait=20):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "heloe-social/1.0"})
            with urllib.request.urlopen(req, timeout=20) as r:
                if r.status == 200:
                    return True
        except Exception:
            pass
        time.sleep(wait)
    return False


def main(date):
    settings = jload(os.path.join(ROOT, "config", "settings.json"), {})
    chcfg = jload(os.path.join(ROOT, "config", "channels.json"), {})
    plan = jload(os.path.join(ROOT, "content", date, "plan.json"), None)
    result_path = os.path.join(ROOT, "content", date, "publish-result.json")
    pub_path = os.path.join(ROOT, "data", "published.json")
    published = jload(pub_path, {})
    result = {"date": date, "ran_at": datetime.now(timezone.utc).isoformat(), "scheduled": [], "skipped": [], "errors": []}

    def finish(code=0):
        json.dump(result, open(result_path, "w"), indent=1, ensure_ascii=False)
        json.dump(published, open(pub_path, "w"), indent=1)
        print(json.dumps(result, indent=1, ensure_ascii=False))
        sys.exit(code)

    if not plan:
        result["errors"].append("no plan")
        finish(1)
    if not settings.get("publishing_enabled", False):
        result["skipped"].append("publishing_enabled is false (master switch)")
        finish(0)
    if plan.get("status") != "approved":
        result["skipped"].append(f"plan status is {plan.get('status')}")
        finish(0)
    errors, warnings = validate(date)
    if errors:
        result["errors"] += ["validation: " + e for e in errors]
        finish(1)

    tz = ZoneInfo(settings.get("timezone_audience", "America/New_York"))
    base = settings["media_base_url"].rstrip("/") + f"/{date}"
    manifest = jload(os.path.join(ROOT, "docs", "media", date, "manifest.json"), {"items": []})
    files = {i["id"]: i for i in manifest["items"]}
    now = datetime.now(timezone.utc)
    log_path = os.path.join(ROOT, "data", "posts.jsonl")

    for post in plan["posts"]:
        pid, plat = post["id"], post["platform"]
        if pid in published:
            result["skipped"].append(f"{pid}: already scheduled ({published[pid]['buffer_id']})")
            continue
        ch = chcfg["channels"][plat].get("buffer_channel_id")
        if not ch:
            result["errors"].append(f"{pid}: no Buffer channel id for {plat} (run the Setup Buffer workflow)")
            continue
        hh, mm = map(int, post["time_local"].split(":"))
        y, mo, d = map(int, date.split("-"))
        due = datetime(y, mo, d, hh, mm, tzinfo=tz).astimezone(timezone.utc)
        if due < now + timedelta(minutes=5):
            if due > now - timedelta(hours=3):
                due = now + timedelta(minutes=10)  # slightly late: post soon rather than drop it
            else:
                result["skipped"].append(f"{pid}: slot {post['time_local']} already passed")
                continue

        assets, media_kinds = [], []
        for mid in post.get("media", []):
            item = files.get(mid)
            if not item:
                result["errors"].append(f"{pid}: rendered file for {mid} not found")
                break
            url = f"{base}/{item['file']}"
            if not settings.get("dry_run") and not url_live(url):
                result["errors"].append(f"{pid}: media not reachable yet: {url}")
                break
            kind = "video" if item["kind"] == "video" else "image"
            assets.append({kind: {"url": url}})
            media_kinds.append(kind)
        else:
            inp = {"text": post["text"], "channelId": ch, "schedulingType": "automatic", "mode": "customScheduled",
                   "dueAt": due.strftime("%Y-%m-%dT%H:%M:%S.000Z"), "assets": assets}
            if settings.get("buffer_ai_assisted_flag"):
                inp["aiAssisted"] = True
            meta = {}
            if plat == "facebook":
                meta["facebook"] = {"type": "post"}
            if plat == "linkedin" and post.get("first_comment"):
                meta["linkedin"] = {"firstComment": post["first_comment"]}
            if meta:
                inp["metadata"] = meta
            if settings.get("dry_run"):
                result["scheduled"].append({"id": pid, "dry_run": True, "input": inp})
                continue
            try:
                r = gql(CREATE, {"input": inp})["createPost"]
            except BufferError as e:
                result["errors"].append(f"{pid}: {e}")
                continue
            if "message" in r:
                result["errors"].append(f"{pid}: {r['message']}")
                continue
            bp = r["post"]
            published[pid] = {"buffer_id": bp["id"], "dueAt": bp["dueAt"], "platform": plat}
            result["scheduled"].append({"id": pid, "buffer_id": bp["id"], "dueAt": bp["dueAt"]})
            rec = {"date": date, "id": pid, "platform": plat, "buffer_id": bp["id"], "due_at": bp["dueAt"],
                   "pillar": post.get("pillar"), "format": post.get("format"), "hook_type": post.get("hook_type"),
                   "media": media_kinds[0] if media_kinds else "text", "topic": plan.get("topic_of_day", {}).get("title"),
                   "text": post["text"]}
            with open(log_path, "a") as f:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            time.sleep(1)

    finish(1 if result["errors"] else 0)


if __name__ == "__main__":
    main(sys.argv[1])
