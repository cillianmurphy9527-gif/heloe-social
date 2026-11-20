---
name: weekly-review
description: Runs Heloe's weekly social media retrospective as Growth Analyst: analyzes Buffer metrics joined with the post log by platform, pillar, format, hook type, media and time slot, compares against cold-start targets, updates playbook/learnings.md with concrete rules, and reports to the founder in Chinese. Use for "weekly review", "how are the accounts doing", "复盘", "这周数据怎么样", or when a scheduled task asks for the Heloe weekly review.
---

# Weekly review (Growth Analyst)

## 0. Workspace
Open the `heloe-social` repo the same way as the daily-content-run skill (add_repo with push access, clone to `~/heloe-social`, `git pull --rebase`).

## 1. Data
- `data/performance.csv`: one row per published post with pillar, format, hook_type, media, due_at and metrics (impressions, reactions, comments, shares, reposts, engagementRate, `eng_rate_calc`).
- `data/metrics_history.jsonl`: daily snapshots for growth curves.
- `data/posts.jsonl`: full text of every post.
- Refresh first: call the Buffer connector's `list_posts` (organization id in `config/channels.json`, status `sent`, dueAt in the last 14 days, `includeMetrics: true`, page through with `after`), save the posts to `/tmp/metrics.json`, and run `python3 scripts/ingest_metrics.py /tmp/metrics.json`. Use `get_aggregated_post_metrics` per channel for weekly totals and week-over-week comparison (free plan: start date within the last 31 days). Metrics lag up to ~24 h, so exclude posts younger than 48 h from judgments.

Analyze with Python (pandas if available, else csv). Engagement rate = engagements / impressions; when impressions are missing, compare raw engagements only within the same platform.

## 2. Analysis
1. Per platform: posts, impressions, engagements, median engagement rate, week-over-week change.
2. Breakdowns per platform by pillar, format, hook_type, media (video / image / text) and time slot. Report n for every cell; mark cells with n < 3 as "insufficient data".
3. Top 3 and bottom 3 posts per platform with a one-line hypothesis each (hook, topic, format, timing).
4. Progress against the 30-day targets in `playbook/strategy.md` section 6.
5. Follower trend if available (Buffer channel data or founder-provided numbers).

## 3. Decisions (max 3 per week)
Follow strategy.md section 7: judge a format only after >= 5 posts on that platform; change one variable at a time; reallocate slots away from the bottom 30% of formats after week 2.
Allowed levers: `config/pillars.json` (shares, weekly calendar formats), `config/channels.json` (slot times), `playbook/hashtags.json` (promote/demote tags), and new Active rules in `playbook/learnings.md`.
Each decision: what changes, why (numbers), how we will know next week.

## 4. Write back
- `playbook/learnings.md`: rewrite the **Active rules** list (keep it under 12 rules, remove ones the data no longer supports) and prepend this week's entry to the **Weekly log**.
- Apply config changes. Run `python3 -m json.tool` on every JSON file you touched.
- Commit: `git add playbook config && git commit -m "weekly review: <week>" && git pull --rebase && git push`.

## 5. Report to the founder (Chinese)
Five short sections: this week's numbers per platform; what worked; what did not; the changes made; what the founder can do this week (e.g., engagement habits, profile fixes, ideas for founder-notes). Keep it under 300 Chinese characters per section, use a small table for numbers. In a scheduled run deliver it with `SendUserMessage` as well as the final reply.
