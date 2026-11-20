#!/usr/bin/env python3
"""Record the outcome of a Buffer create_post (or an approval decision) in the repo logs.

Usage:
  python3 scripts/record_publish.py D scheduled <post_id> <buffer_post_id> <dueAt>
  python3 scripts/record_publish.py D error <post_id> "<message>"
  python3 scripts/record_publish.py D pending <post_id> [<post_id> ...]     # sent to the founder for review
  python3 scripts/record_publish.py D approve <post_id> [<post_id> ...]     # founder said OK
  python3 scripts/record_publish.py D reject <post_id> [<post_id> ...]      # founder said no
Updates data/published.json, data/posts.jsonl, content/D/publish-result.json, content/D/approvals.json.
"""
import json, os, sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def jload(p, default):
    return json.load(open(p)) if os.path.exists(p) else default


def jsave(p, obj):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    json.dump(obj, open(p, "w"), indent=1, ensure_ascii=False)


def main(date, action, *rest):
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    res_p = os.path.join(ROOT, "content", date, "publish-result.json")
    apr_p = os.path.join(ROOT, "content", date, "approvals.json")
    pub_p = os.path.join(ROOT, "data", "published.json")
    res = jload(res_p, {"date": date, "scheduled": [], "skipped": [], "errors": []})
    apr = jload(apr_p, {"approved": [], "pending": [], "rejected": []})

    if action == "scheduled":
        pid, bid, due = rest[:3]
        plan = jload(os.path.join(ROOT, "content", date, "plan.json"), {})
        post = next((p for p in plan.get("posts", []) if p["id"] == pid), {})
        pub = jload(pub_p, {})
        pub[pid] = {"buffer_id": bid, "dueAt": due, "platform": post.get("platform"), "recorded_at": now}
        jsave(pub_p, pub)
        res["scheduled"].append({"id": pid, "buffer_id": bid, "dueAt": due})
        media = "text"
        for m in post.get("media", []):
            v = next((x for x in plan.get("visuals", []) if x["id"] == m), {})
            media = "video" if v.get("kind") == "video" else "image"
        rec = {"date": date, "id": pid, "platform": post.get("platform"), "buffer_id": bid, "due_at": due,
               "pillar": post.get("pillar"), "format": post.get("format"), "hook_type": post.get("hook_type"), "media": media,
               "topic": plan.get("topic_of_day", {}).get("title"), "text": post.get("text")}
        with open(os.path.join(ROOT, "data", "posts.jsonl"), "a") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        apr["pending"] = [p for p in apr["pending"] if p != pid]
    elif action == "error":
        pid, msg = rest[0], " ".join(rest[1:])
        res["errors"].append(f"{pid}: {msg} ({now})")
    elif action in ("pending", "approve", "reject"):
        key = {"pending": "pending", "approve": "approved", "reject": "rejected"}[action]
        for pid in rest:
            for k in ("pending", "approved", "rejected"):
                apr[k] = [p for p in apr[k] if p != pid]
            apr[key].append(pid)
        apr.setdefault("log", []).append({"at": now, "action": action, "posts": list(rest)})
        jsave(apr_p, apr)
    else:
        sys.exit(f"unknown action {action}")
    jsave(res_p, res)
    if action in ("scheduled",):
        jsave(apr_p, apr)
    print("ok")


if __name__ == "__main__":
    main(*sys.argv[1:])
