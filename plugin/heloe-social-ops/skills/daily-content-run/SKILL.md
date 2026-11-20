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
- Fresh numbers: call the Buffer connector's `list_posts` (organization from `config/channels.json`, status `sent`, dueAt in the last 7 days, `includeMetrics: true`), save the results to `/tmp/metrics.json` and run `python3 scripts/ingest_metrics.py /tmp/metrics.json`. Skip this step if Buffer is unavailable.

## 2. Scout
Spawn the **trend-scout** agent (subagent type `heloe-social-ops:trend-scout`; if that type is unavailable, spawn a general-purpose agent and tell it to read and follow `plugin/heloe-social-ops/agents/trend-scout.md` in the repo). Pass `REPO`, `D`. It writes `content/D/scout.json`.

## 3. Editorial brief (you decide)
Write `content/D/brief.json` following `references/plan-schema.md`:
- Topic of the day: usually the scout's top pick; override it when the pick is unsafe, repeats a topic used in the last 7 days, or cannot bridge to Heloe's positioning.
- The slate: one entry per slot in `channels.json` for D's weekday, capped by `settings.max_posts_per_day`. For each: platform, `time_local`, pillar, format, hook direction (one line), media assignment.
- Follow the weekly calendar for the LinkedIn pillar/format and X media; follow `pillars.json.daily_x_mix` for X slots; Facebook reuses the day's main asset and angle.
- Apply Active rules from `learnings.md`. During cold start (first 14 days of `data/posts.jsonl`), make sure formats rotate so every format gets tested.
- Media needed today: on video days, one cinematic 16:9 video (1920x1080, see the visual-design skill) shared by LinkedIn/Facebook/X; on image days, a 1080x1350 cover for LinkedIn/Facebook and, when X carries media, a 1600x900 cover. Posts carrying the video need the founder's approval, so on video days also give each platform at least one image or text post.

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

## 8. Ship media
```bash
cd ~/heloe-social && git add content/D docs/media/D && git commit -m "plan: D" && git pull --rebase && git push
python3 scripts/wait_deploy.py $(git rev-parse HEAD)     # waits until GitHub Pages serves the media (usually 2-4 min)
```
If the deploy fails, report it and stop: do not schedule posts whose media is not live.

## 9. Schedule through the Buffer connector
1. Run `python3 scripts/prepare_publish.py D`. It prints `ready` (exact `create_post` arguments), `awaiting_approval` and `skipped`.
2. For each `ready` item call the Buffer connector's `create_post` with its `payload` unchanged. Then record it:
   `python3 scripts/record_publish.py D scheduled <post_id> <returned post id> <returned dueAt>`.
   On an error: `python3 scripts/record_publish.py D error <post_id> "<message>"`. If Buffer rejects media, retry once after 60 s (Pages can lag), then give up on that post.
3. **Videos wait for the founder.** For each `awaiting_approval` item: send the founder the video file (`SendUserFile` with the `local_files` path) together with the post text and the planned time, and ask for "OK", a change request, or "no". Record `python3 scripts/record_publish.py D pending <post_id>`. Never schedule a video without an explicit OK; the social-ops-control skill handles the reply.
4. Commit and push `data/` and `content/D/` again.

## 10. Report (Chinese, short)
Send the founder a brief: today's topic and why; each scheduled post (platform, Beijing time and New York time, first line); the video waiting for approval (with the file); anything dropped or rejected and why; yesterday's errors; today's engagement brief. In a scheduled run, deliver it with `SendUserMessage` (and `PushNotification` if available) as well as the final reply.

## Failure handling
- A failed agent: retry once with a narrower prompt; if it fails again, continue with fewer posts rather than none.
- Rendering unavailable in this session: commit the plan without media files and note it; the workflow renders missing media (without visual QA, so prefer cover templates over video that day).
- Never fabricate data to fill a slot. An empty slot is better than a wrong post.
