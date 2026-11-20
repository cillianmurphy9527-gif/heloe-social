#!/usr/bin/env python3
"""Join per-post metrics read through the Buffer connector with data/posts.jsonl.

Input: a JSON file with a list of posts as returned by the Buffer connector's list_posts(includeMetrics=true),
either the raw objects or compact ones: [{"id": "...", "channelService": "linkedin", "dueAt": "...",
"metrics": [{"type": "impressions", "value": 120}, ...] or {"impressions": 120, ...}}]

Usage: python3 scripts/ingest_metrics.py /tmp/metrics.json
Writes data/metrics_latest.json, data/performance.csv and appends a snapshot line to data/metrics_history.jsonl.
"""
import csv, json, os, sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COLS = ["impressions", "reach", "views", "reactions", "likes", "comments", "shares", "reposts", "quotes", "saves", "clicks", "engagementRate"]
ENG = ["reactions", "likes", "comments", "shares", "reposts", "quotes", "saves"]


def norm(raw):
    items = raw.get("edges", raw) if isinstance(raw, dict) else raw
    out = {}
    for it in items:
        n = it.get("node", it)
        m = n.get("metrics") or {}
        if isinstance(m, list):
            m = {x["type"]: x.get("value") for x in m}
        out[n["id"]] = {**m, "_platform": n.get("channelService"), "_dueAt": n.get("dueAt"), "_updated": n.get("metricsUpdatedAt")}
    return out


def main(path):
    metrics = norm(json.load(open(path)))
    prev_p = os.path.join(ROOT, "data", "metrics_latest.json")
    allm = json.load(open(prev_p)) if os.path.exists(prev_p) else {}
    allm.update(metrics)
    json.dump(allm, open(prev_p, "w"), indent=1)

    log = os.path.join(ROOT, "data", "posts.jsonl")
    posts = [json.loads(l) for l in open(log) if l.strip()] if os.path.exists(log) else []
    rows = []
    for p in posts:
        m = allm.get(p.get("buffer_id"), {})
        row = {k: p.get(k) for k in ["date", "id", "platform", "pillar", "format", "hook_type", "media", "due_at"]}
        row["hook"] = (p.get("text") or "").split("\n")[0][:120]
        for c in COLS:
            row[c] = m.get(c, "")
        imp = float(m.get("impressions") or m.get("views") or 0)
        eng = sum(float(m.get(k) or 0) for k in ENG)
        row["engagements"] = eng
        row["eng_rate_calc"] = round(eng / imp * 100, 2) if imp else ""
        rows.append(row)
    with open(os.path.join(ROOT, "data", "performance.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else ["date"])
        w.writeheader()
        w.writerows(rows)

    snap = {"at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "posts_with_metrics": len(metrics)}
    for plat in sorted({m["_platform"] for m in metrics.values() if m.get("_platform")}):
        ms = [m for m in metrics.values() if m["_platform"] == plat]
        snap[plat] = {"posts": len(ms), "impressions": sum(float(m.get("impressions") or 0) for m in ms),
                      "engagements": sum(float(m.get(k) or 0) for m in ms for k in ENG)}
    with open(os.path.join(ROOT, "data", "metrics_history.jsonl"), "a") as f:
        f.write(json.dumps(snap) + "\n")
    print(json.dumps(snap, indent=1))
    print(f"performance.csv rows: {len(rows)}")


if __name__ == "__main__":
    main(sys.argv[1])
