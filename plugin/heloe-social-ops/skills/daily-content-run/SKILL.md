---
name: daily-content-run
description: Runs Heloe's daily social media production as Editor-in-Chief, coordinating the Trend Scout, Copywriter, Visual Designer and Brand Editor agents to turn today's trending topics into approved LinkedIn, X and Facebook posts with covers and video, then hands them to the GitHub publishing pipeline. Use for "run today's content", "daily social run", "生成今天的社媒内容", "今天的帖子", or when a scheduled task asks for the Heloe daily run.
---

# Daily content run (Editor-in-Chief)

Act as Heloe's Editor-in-Chief. Coordinate specialist agents, make the editorial calls yourself, and ship one approved plan per posting day. All content is written in US English; the final report to the founder is in Chinese.

## 0. Workspace
1. Locate the operations repo `heloe-social`. Use the `owner/repo` given in the task prompt; otherwise call `list_repos` with query `heloe-social`.
2. If it is not cloned yet: call `add_repo` with `access: "push"`, run the clone command it returns into `~/heloe-social`, and work there (`REPO=~/heloe-social`). Run `git pull --rebase` if it already exists.
3. Set `git config user.name "heloe-editor"` and `git config user.email "bot@users.noreply.github.com"` in the repo.
4. Pick the target date `D`: the current date in America/New_York if it is before 06:00 there, otherwise the next day. Allow an explicit date from the prompt to override.
5. Stop early, and say why in the report, when:
   - `config/settings.json` has `publishing_enabled: false` (paused by the founder), or
   - `content/D/plan.json` already exists with `status: approved` (already done; just report its status and `publish-result.json` if present).
6. Check the previous day's `content/<D-1>/publish-result.json`. Carry any errors into the report.

## 1. Load context (read, do not summarize back)
- `playbook/strategy.md`, `playbook/platform-rules.md`, `playbook/learnings.md` (its **Active rules** override defaults), `playbook/founder-notes.md`, `playbook/hashtags.json`
- `config/pillars.json` (weekly calendar entry for D's weekday), `config/channels.json` (slots for that weekday), `config/settings.json`
- Last 14 days of `data/posts.jsonl` and, if present, `data/performance.csv` (note the top 3 and bottom 3 posts by engagement rate)

## 2. Scout
Spawn the **trend-scout** agent (subagent type `heloe-social-ops:trend-scout`; if that type is unavailable, spawn a general-purpose agent and tell it to read and follow `plugin/heloe-social-ops/agents/trend-scout.md` in the repo). Pass `REPO`, `D`. It writes `content/D/scout.json`.

## 3. Editorial brief (you decide)
Write `content/D/brief.json` following `references/plan-schema.md`:
- Topic of the day: usually the scout's top pick; override it when the pick is unsafe, repeats a topic used in the last 7 days, or cannot bridge to Heloe's positioning.
- The slate: one entry per slot in `channels.json` for D's weekday, capped by `settings.max_posts_per_day`. For each: platform, `time_local`, pillar, format, hook direction (one line), media assignment.
- Follow the weekly calendar for the LinkedIn pillar/format and X media; follow `pillars.json.daily_x_mix` for X slots; Facebook reuses the day's main asset and angle.
- Apply Active rules from `learnings.md`. During cold start (first 14 days of `data/posts.jsonl`), make sure formats rotate so every format gets tested.
- Media needed today: one portrait asset (1080x1350) for LinkedIn/Facebook (cover or video per calendar) and, when X carries media, a 1600x900 cover (X may also reuse the video).

## 4. Create (run both agents in parallel)
- **copywriter** (`heloe-social-ops:copywriter`, fallback file `agents/copywriter.md`): writes `content/D/copy.json`.
- **visual-designer** (`heloe-social-ops:visual-designer`, fallback `agents/visual-designer.md`): writes `content/D/visuals.json` and renders into `docs/media/D/`.

## 5. Assemble and validate
1. Merge brief + copy + visuals into `content/D/plan.json` with `status: "draft"` (schema in `references/plan-schema.md`).
2. Run `python3 scripts/validate_plan.py D`. Fix errors yourself when trivial (length, hashtag count, slot time); otherwise send the post back to the copywriter once.

## 6. Review
Spawn the **brand-editor** agent (`heloe-social-ops:brand-editor`, fallback `agents/brand-editor.md`). It has not seen the drafting and must stay independent: give it only `REPO` and `D`. It writes `content/D/review.json`.
- Apply every `revise` fix it gives (exact replacement text), re-render a visual if its text changed, and re-run the validator.
- Drop posts marked `drop`. Do not argue the editor out of a factual or safety objection.
- Set `plan.review` from the review file. Set `status: "approved"` only if the overall score is >= `settings.min_editor_score` and at least one post remains; otherwise `status: "rejected"` (nothing publishes) and explain in the report.

## 7. Engagement brief
Add 3-5 items to `plan.engagement_brief` for the founder's 15 minutes of manual engagement: which conversation to join (topic or community, from the scout's findings), and a 1-2 sentence comment idea. Platforms forbid automated replies, so these are suggestions for a human.

## 8. Ship
```bash
cd ~/heloe-social && git add content/D docs/media/D && git commit -m "plan: D" && git pull --rebase && git push
```
The push triggers the **Render and publish** workflow, which deploys media to GitHub Pages and schedules posts in Buffer at the planned New York times. Do not call Buffer `create_post` yourself unless the founder explicitly asks; the pipeline is the single publisher so nothing is posted twice.

## 9. Report (Chinese, short)
Send the founder a brief: today's topic and why; each scheduled post (platform, New York time and Beijing time, first line of text); which visuals were made; anything dropped or rejected and why; yesterday's pipeline errors; today's engagement brief. In a scheduled run, deliver it with `SendUserMessage` (or `PushNotification` if available) as well as the final reply.

## Failure handling
- A failed agent: retry once with a narrower prompt; if it fails again, continue with fewer posts rather than none.
- Rendering unavailable in this session: commit the plan without media files and note it; the workflow renders missing media (without visual QA, so prefer cover templates over video that day).
- Never fabricate data to fill a slot. An empty slot is better than a wrong post.
