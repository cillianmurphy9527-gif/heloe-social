#!/usr/bin/env python3
"""Collect today's candidate topics from Hacker News and Google News into trends/<date>.json.

Runs in GitHub Actions (full internet). Standard library only.
Reddit is collected separately (see the reddit-scan skill) because Reddit closed public API/RSS access in 2026.
"""
import json, os, sys, time, urllib.parse, urllib.request, xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = {"User-Agent": "heloe-social-trends/1.0 (+https://heloe.io)"}


def get(url, timeout=20):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def hackernews(cfg):
    since = int(time.time() - cfg["lookback_hours"] * 3600)
    seen, items = set(), []
    queries = [None] + cfg["queries"]  # None = front page
    for q in queries:
        params = {"tags": "front_page"} if q is None else {
            "query": q, "tags": "story",
            "numericFilters": f"created_at_i>{since},points>{cfg['min_points']}", "hitsPerPage": 20}
        try:
            data = json.loads(get("https://hn.algolia.com/api/v1/search?" + urllib.parse.urlencode(params)))
        except Exception as e:  # keep going on partial failure
            print(f"[hn] {q}: {e}", file=sys.stderr)
            continue
        for h in data.get("hits", []):
            if h["objectID"] in seen or not h.get("title"):
                continue
            seen.add(h["objectID"])
            age_h = max(1, (time.time() - h.get("created_at_i", time.time())) / 3600)
            pts, com = h.get("points") or 0, h.get("num_comments") or 0
            items.append({
                "source": "hackernews", "query": q or "front_page", "title": h["title"],
                "url": h.get("url") or f"https://news.ycombinator.com/item?id={h['objectID']}",
                "discussion_url": f"https://news.ycombinator.com/item?id={h['objectID']}",
                "points": pts, "comments": com, "age_hours": round(age_h, 1),
                "heat": round((pts + 2 * com) / (age_h + 2) ** 0.8, 2),
            })
        time.sleep(0.3)
    return items


def google_news(cfg):
    items, seen = [], {}
    for q in cfg["queries"]:
        url = "https://news.google.com/rss/search?" + urllib.parse.urlencode(
            {"q": f'"{q}" when:{cfg["window"]}', "hl": cfg["lang"], "gl": cfg["country"],
             "ceid": f'{cfg["country"]}:{cfg["lang"].split("-")[0]}'})
        try:
            root = ET.fromstring(get(url))
        except Exception as e:
            print(f"[gnews] {q}: {e}", file=sys.stderr)
            continue
        for it in root.iter("item"):
            title = (it.findtext("title") or "").strip()
            key = title.lower()[:90]
            if not title:
                continue
            if key in seen:
                seen[key]["queries"].append(q)
                continue
            src = it.find("source")
            rec = {"source": "google_news", "queries": [q], "title": title, "url": it.findtext("link"),
                   "publisher": src.text if src is not None else "", "published": it.findtext("pubDate")}
            seen[key] = rec
            items.append(rec)
        time.sleep(0.5)
    for r in items:  # stories that match several queries are more central to our niche
        r["heat"] = len(r["queries"])
    return items


def main():
    cfg = json.load(open(os.path.join(ROOT, "config", "sources.json")))
    now = datetime.now(timezone.utc)
    date = sys.argv[1] if len(sys.argv) > 1 else now.astimezone(timezone(timedelta(hours=-5))).strftime("%Y-%m-%d")
    hn = sorted(hackernews(cfg["hackernews"]), key=lambda x: -x["heat"])[:60]
    gn = sorted(google_news(cfg["google_news"]), key=lambda x: -x["heat"])[:80]
    out = {"date": date, "collected_at": now.isoformat(), "counts": {"hackernews": len(hn), "google_news": len(gn)},
           "hackernews": hn, "google_news": gn}
    os.makedirs(os.path.join(ROOT, "trends"), exist_ok=True)
    path = os.path.join(ROOT, "trends", f"{date}.json")
    json.dump(out, open(path, "w"), indent=1, ensure_ascii=False)
    print(f"wrote {path}: {out['counts']}")
    if not hn and not gn:
        sys.exit("no trend items collected")


if __name__ == "__main__":
    main()
