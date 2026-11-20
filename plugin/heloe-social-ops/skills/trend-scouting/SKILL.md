---
name: trend-scouting
description: Finds and scores the day's trending topics for Heloe's audience (founders, SDRs, sales leaders, B2B SaaS) from Hacker News, Google News, Product Hunt, Reddit scans and web search, producing content/DATE/scout.json. Use for "today's hot topics", "what is the sales community talking about", "选题", "今日热点", or as step 2 of the daily content run.
---

# Trend scouting

Inputs: `REPO` (repo path) and `D` (date). Output: `REPO/content/D/scout.json`.

## 1. Gather candidates (aim for 25-40)
1. `trends/D.json` (collected by GitHub Actions): Hacker News stories (`heat` = points/comments velocity) and Google News stories (`heat` = number of niche queries matched). If the file for D is missing, use the newest file in `trends/`.
2. `trends/reddit-D.json` if present (from the Reddit scan): subreddit top posts with scores, comment counts and paraphrased gists. Treat high comment counts as strong heat signals; Reddit is the best read on practitioner pain.
3. Product Hunt (if the Product Hunt connector is available): today's leaderboard; keep launches in sales, marketing, email, AI agents, productivity.
4. Web search, 3-6 queries, recent results only, for example: `cold email news this week`, `sales teams AI SDR backlash`, `Gmail Outlook bulk sender rules update`, `LinkedIn algorithm change sales`, `startup funding this week`, `indiehackers outbound`. Use `WebFetch` on the 3-5 most promising results to confirm what they actually say.

Never list a URL you did not retrieve. Record the date of each source; drop anything older than 7 days unless it is evergreen data for the Data pillar.

## 2. Filter (hard gates)
Drop topics about tragedies, deaths, wars, elections and partisan politics, named people's layoffs or legal trouble, NSFW, crypto pumping, or anything where joining in would look like exploiting bad news. Drop topics with no plausible bridge to selling, outbound, founders or go-to-market.

## 3. Score
Use `references/scoring.md`. Score every surviving candidate, then pick the top 5. Prefer a topic with a clear bridge to **timing/signals** over a slightly hotter generic one.

## 4. Write scout.json
```json
{
  "date": "D",
  "sources_checked": { "hackernews": 0, "google_news": 0, "reddit": 0, "product_hunt": 0, "web": 0 },
  "source_failures": ["..."],
  "top": [
    {
      "rank": 1, "title": "short neutral title", "summary": "2 sentences in your own words",
      "why_now": "what happened in the last 48h", "scores": { "heat": 8, "relevance": 9, "bridge": 8, "freshness": 9, "total": 8.5 },
      "best_pillar": "trends", "angles": ["angle for LinkedIn", "angle for X", "contrarian angle"],
      "facts": [ { "claim": "paraphrased fact or number", "source": "https://...", "source_date": "2026-11-20" } ],
      "community_pulse": "paraphrase of how practitioners feel (no usernames, no verbatim quotes)",
      "sources": ["https://..."]
    }
  ],
  "evergreen_backups": [ { "title": "...", "pillar": "infra", "angle": "..." } ]
}
```
Add 2-3 `evergreen_backups` (timeless pillar ideas) so the editor has options on slow news days.

## Rules
- Paraphrase. Quote at most a short phrase (under 15 words) and only when the exact words matter.
- Reddit: never record usernames; describe sentiment ("founders on r/sales are split on...").
- Numbers must carry their exact source URL and date in `facts`.
