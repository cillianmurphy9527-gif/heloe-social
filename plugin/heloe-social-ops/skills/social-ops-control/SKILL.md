---
name: social-ops-control
description: Founder controls for Heloe's social automation: pause or resume publishing, show what was posted or scheduled, check pipeline health and errors, delete a scheduled post, change posting times or cadence. Use for "pause posting", "resume", "what did we post today", "is the pipeline working", "暂停发布", "恢复发布", "今天发了什么", "删掉那条", "改发布时间".
---

# Social ops control

Open the `heloe-social` repo (add_repo with push access → clone to `~/heloe-social` → `git pull --rebase`). Answer the founder in Chinese.

## Pause / resume
Edit `config/settings.json` → `publishing_enabled` (`false` pauses: the daily run stops early and the publisher refuses to schedule). Commit and push with a clear message. Already-scheduled Buffer posts are not affected by the switch: if the founder wants them gone too, list them via the Buffer connector (`list_posts`, status scheduled) and delete only after the founder confirms the list, since deletion cannot be undone.

## Status
- Today's and tomorrow's `content/<D>/plan.json` (status, posts, times) and `publish-result.json` (scheduled / skipped / errors).
- Latest `trends/` files (was collection working?), latest `data/metrics_history.jsonl` line.
- If the Buffer connector is available, cross-check scheduled posts for the next 48 h.
Present New York and Beijing times side by side.

## Remove or edit one post
Find it in `data/published.json` (post id → Buffer id). Use the Buffer connector (`get_post`, then `edit_post` or `delete_post`) after the founder confirms. Note the change in the day's `publish-result.json` and commit.

## Change cadence or times
Edit `config/channels.json` slots (New York local times) or `settings.max_posts_per_day`; validate JSON; commit and push. Mention that the next daily run picks it up.

## Brand updates
When the founder sends new logo files, colors or fonts: save logos to `brand/` (SVG preferred), update `config/brand.json`, render the test plan with `render/render.sh <date>` and show the contact sheet before committing.
