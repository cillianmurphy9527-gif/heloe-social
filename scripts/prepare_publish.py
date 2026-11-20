#!/usr/bin/env python3
"""Build the exact Buffer `create_post` payloads for an approved day, for Claude to send through the Buffer connector.

Usage: python3 scripts/prepare_publish.py 2026-11-23 [--include-approved-only]
Prints JSON: {"ready": [...], "awaiting_approval": [...], "skipped": [...], "errors": [...]}
  ready[i] = {"post_id", "platform", "payload": {...create_post arguments...}}

- Validates the plan first (scripts/validate_plan.py); stops on errors.
- Skips posts already recorded in data/published.json.
- Posts whose media kind is in settings.approval_required_for go to awaiting_approval unless
  content/<D>/approvals.json lists them under "approved".
- dueAt is the slot in America/New_York with its UTC offset. If the slot has passed, the post moves to
  15 minutes from now when that is still the same New York day; otherwise it is skipped.
After each successful create_post, run scripts/record_publish.py.
"""
import json, os, sys
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from validate_plan import validate

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def jload(p, default):
    return json.load(open(p)) if os.path.exists(p) else default


def alt_text(v):
    f = v.get("fields", {})
    parts = [f.get("kicker"), f.get("stat"), f.get("headline") or f.get("title") or f.get("quote"), f.get("caption")]
    if f.get("items"):
        parts.append("; ".join(f["items"]))
    txt = ". ".join(str(p).replace("*", "") for p in parts if p)
    return (txt or "Heloe graphic")[:900]


def main(date):
    out = {"date": date, "ready": [], "awaiting_approval": [], "skipped": [], "errors": []}
    settings = jload(os.path.join(ROOT, "config", "settings.json"), {})
    ch = jload(os.path.join(ROOT, "config", "channels.json"), {})
    plan = jload(os.path.join(ROOT, "content", date, "plan.json"), None)
    published = jload(os.path.join(ROOT, "data", "published.json"), {})
    approvals = jload(os.path.join(ROOT, "content", date, "approvals.json"), {"approved": [], "pending": [], "rejected": []})
    manifest = jload(os.path.join(ROOT, "docs", "media", date, "manifest.json"), {"items": []})
    files = {i["id"]: i for i in manifest["items"]}

    def done(code=0):
        print(json.dumps(out, indent=1, ensure_ascii=False))
        sys.exit(code)

    if not plan:
        out["errors"].append("no plan.json")
        done(1)
    if not settings.get("publishing_enabled"):
        out["skipped"].append("publishing paused (settings.publishing_enabled = false)")
        done()
    if plan.get("status") != "approved":
        out["skipped"].append(f"plan status is {plan.get('status')}")
        done()
    errs, _ = validate(date)
    if errs:
        out["errors"] += errs
        done(1)

    tz = ZoneInfo(settings.get("timezone_audience", "America/New_York"))
    now = datetime.now(timezone.utc)
    base = settings["media_base_url"].rstrip("/") + f"/{date}"
    visuals = {v["id"]: v for v in plan.get("visuals", [])}
    need_ok = set(settings.get("approval_required_for", []))

    for post in plan["posts"]:
        pid, plat = post["id"], post["platform"]
        if pid in published:
            out["skipped"].append(f"{pid}: already scheduled")
            continue
        if pid in approvals.get("rejected", []):
            out["skipped"].append(f"{pid}: rejected by founder")
            continue
        chan = ch["channels"][plat].get("buffer_channel_id")
        if not chan:
            out["errors"].append(f"{pid}: no channel id for {plat}")
            continue
        assets, kinds, bad = [], [], False
        for mid in post.get("media", []):
            item, vis = files.get(mid), visuals.get(mid, {})
            if not item:
                out["errors"].append(f"{pid}: media {mid} not rendered")
                bad = True
                break
            url = f"{base}/{item['file']}"
            if item["kind"] == "video":
                assets.append({"video": {"url": url}})
                kinds.append("video")
            else:
                assets.append({"image": {"url": url, "metadata": {"altText": alt_text(vis)}}})
                kinds.append("image")
        if bad:
            continue
        if need_ok.intersection(kinds) and pid not in approvals.get("approved", []):
            out["awaiting_approval"].append({"post_id": pid, "platform": plat, "time_local": post["time_local"],
                                             "media": [f"{base}/{files[m]['file']}" for m in post.get("media", [])],
                                             "local_files": [f"docs/media/{date}/{files[m]['file']}" for m in post.get("media", [])],
                                             "text": post["text"]})
            continue
        y, mo, d = map(int, date.split("-"))
        hh, mm = map(int, post["time_local"].split(":"))
        due = datetime(y, mo, d, hh, mm, tzinfo=tz)
        if due <= now + timedelta(minutes=5):
            alt = (now + timedelta(minutes=15)).astimezone(tz).replace(second=0, microsecond=0)
            if alt.date() == due.date():
                due = alt
            else:
                out["skipped"].append(f"{pid}: slot {post['time_local']} New York time has passed")
                continue
        payload = {"channelId": chan, "schedulingType": "automatic", "mode": "customScheduled",
                   "dueAt": due.isoformat(timespec="seconds"), "text": post["text"]}
        if assets:
            payload["assets"] = assets
        meta = {}
        if plat == "facebook":
            meta["facebook"] = {"type": "post"}
        if plat == "linkedin" and post.get("first_comment"):
            meta["linkedin"] = {"firstComment": post["first_comment"]}
        if meta:
            payload["metadata"] = meta
        out["ready"].append({"post_id": pid, "platform": plat, "due_beijing": due.astimezone(ZoneInfo("Asia/Shanghai")).strftime("%m-%d %H:%M"),
                             "payload": payload})
    done(1 if out["errors"] else 0)


if __name__ == "__main__":
    main(sys.argv[1])
