---
name: reddit-scan
description: Reads today's top Reddit discussions in Heloe's niche subreddits through the founder's own Chrome (Claude in Chrome), summarizes them in paraphrase, and saves trends/reddit-<date>.json to the heloe-social repo for the Trend Scout. Use for "scan Reddit", "Reddit 热帖", or when a scheduled task asks for the Heloe Reddit scan.
---

# Reddit scan (via the founder's Chrome)

Reddit closed self-service API access in 2025, stopped accepting new API requests on Oct 31, 2026 and retired RSS on Nov 13, 2026, so cloud scripts cannot read it. This scan reads Reddit the way a person would, in the founder's signed-in Chrome, at low volume, for topic research only.

## Preconditions
- Claude in Chrome tools are available (load the `chrome-browser` skill first if listed). If no browser is reachable, write nothing, report "Reddit scan skipped: browser unavailable", and stop. The daily run works without this file.
- If reddit.com does not load (network/VPN), stop after the first failure and report it.

## Steps
1. Open the `heloe-social` repo (add_repo with push access, clone to `~/heloe-social`, `git pull --rebase`). Read `config/sources.json` → `reddit` (subreddits, `per_sub`).
2. Determine `D` = today's date in America/New_York (or the next day if it is past 18:00 there).
3. In a new tab, for each subreddit open `https://www.reddit.com/r/<sub>/top/?t=day` and read the page text. Record for up to `per_sub` posts: title, score, comment count, flair, post URL, age. At most 14 page loads in total; pause a few seconds between pages.
4. Open the 3 discussions with the most comments across all subreddits and capture the general sentiment and the 2-3 main arguments, **in your own words**.
5. Write `trends/reddit-D.json`:
```json
{ "date": "D", "scanned_at": "ISO time", "status": "ok",
  "posts": [ { "subreddit": "sales", "title": "...", "score": 0, "comments": 0, "url": "https://www.reddit.com/...", "gist": "one-line paraphrase" } ],
  "discussions": [ { "url": "...", "theme": "...", "sentiment": "paraphrase of the debate", "arguments": ["...", "..."] } ] }
```
6. Commit and push: `git add trends && git commit -m "reddit: D" && git pull --rebase && git push`.

## Rules
- Never record usernames or copy comments verbatim; paraphrase.
- Do not log in, vote, post, comment, message or join anything. Read only.
- Close the tab when done.
