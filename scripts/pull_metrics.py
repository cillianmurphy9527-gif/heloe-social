#!/usr/bin/env python3
"""Pull per-post metrics for the last N days from Buffer and join them with data/posts.jsonl.

Outputs:
  data/metrics_latest.json     buffer_id -> {metric_type: value, ...}
  data/performance.csv         one row per post we published (pillar/format/hook joined with metrics)
  data/metrics_history.jsonl   one snapshot line per run (for growth curves)
Usage: python scripts/pull_metrics.py [days=30]
"""
import csv, json, os, sys
from datetime import datetime, timezone, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from buffer import gql

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
Q = """query($first: Int!, $after: String, $input: PostsInput!) {
  posts(first: $first, after: $after, input: $input) {
    edges { node { id dueAt channelId status metrics { type name value unit } metricsUpdatedAt } }
    pageInfo { endCursor hasNextPage }
  }
}"""
COLS = ["impressions", "reach", "views", "reactions", "likes", "comments", "shares", "reposts", "quotes", "saves", "follows", "engagementRate"]


def main(days=30):
    ch = json.load(open(os.path.join(ROOT, "config", "channels.json")))
    org = ch["buffer_organization_id"]
    chan_ids = {v["buffer_channel_id"]: k for k, v in ch["channels"].items() if v.get("buffer_channel_id")}
    start = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    metrics, after = {}, None
    while True:
        data = gql(Q, {"first": 50, "after": after, "input": {
            "organizationId": org, "filter": {"status": ["sent"], "channelIds": list(chan_ids), "startDate": start}}})["posts"]
        for e in data["edges"]:
            n = e["node"]
            m = {x["type"]: x["value"] for x in (n.get("metrics") or [])}
            m.update({"_platform": chan_ids.get(n["channelId"]), "_dueAt": n["dueAt"], "_updated": n.get("metricsUpdatedAt")})
            metrics[n["id"]] = m
        if not data["pageInfo"]["hasNextPage"]:
            break
        after = data["pageInfo"]["endCursor"]

    os.makedirs(os.path.join(ROOT, "data"), exist_ok=True)
    json.dump(metrics, open(os.path.join(ROOT, "data", "metrics_latest.json"), "w"), indent=1)

    posts = []
    log = os.path.join(ROOT, "data", "posts.jsonl")
    if os.path.exists(log):
        posts = [json.loads(l) for l in open(log) if l.strip()]
    rows = []
    for p in posts:
        m = metrics.get(p.get("buffer_id"), {})
        row = {k: p.get(k) for k in ["date", "id", "platform", "pillar", "format", "hook_type", "media", "due_at"]}
        row["hook"] = (p.get("text") or "").split("\n")[0][:120]
        for c in COLS:
            row[c] = m.get(c, "")
        imp = float(m.get("impressions") or m.get("views") or 0)
        eng = sum(float(m.get(k) or 0) for k in ["reactions", "comments", "shares", "reposts", "quotes", "saves"])
        row["engagements"] = eng
        row["eng_rate_calc"] = round(eng / imp * 100, 2) if imp else ""
        rows.append(row)
    with open(os.path.join(ROOT, "data", "performance.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else ["date"])
        w.writeheader()
        w.writerows(rows)

    snap = {"at": datetime.now(timezone.utc).isoformat(), "posts_with_metrics": len(metrics)}
    for plat in set(chan_ids.values()):
        ms = [m for m in metrics.values() if m["_platform"] == plat]
        snap[plat] = {"posts": len(ms), "impressions": sum(float(m.get("impressions") or 0) for m in ms),
                      "engagements": sum(float(m.get(k) or 0) for m in ms for k in ["reactions", "comments", "shares", "reposts"])}
    with open(os.path.join(ROOT, "data", "metrics_history.jsonl"), "a") as f:
        f.write(json.dumps(snap) + "\n")
    print(json.dumps(snap, indent=1))


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 30)
