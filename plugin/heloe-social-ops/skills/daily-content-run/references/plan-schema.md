# content/<D>/ files

## brief.json (Editor-in-Chief)
```json
{
  "date": "2026-11-23",
  "topic_of_day": { "title": "...", "summary": "...", "why_now": "...", "pillar": "trends", "score": 8.1, "sources": ["https://..."] },
  "slate": [
    { "id": "2026-11-23-li-1", "platform": "linkedin", "time_local": "08:30", "pillar": "signals", "format": "teardown",
      "direction": "one line on the angle and hook", "media": ["video-main"] },
    { "id": "2026-11-23-x-1", "platform": "x", "time_local": "09:00", "pillar": "trends", "format": "hot-take", "direction": "...", "media": ["cover-x"] }
  ],
  "media_plan": [
    { "id": "video-main", "kind": "video", "size": "1080x1350", "direction": "..." },
    { "id": "cover-x", "kind": "cover", "size": "1600x900", "direction": "..." }
  ]
}
```
Post ids: `<D>-<li|x|fb>-<n>`. Visual ids: short kebab-case, unique within the day.

## copy.json (Copywriter)
```json
{ "posts": [ { "id": "...", "platform": "linkedin", "text": "...", "first_comment": "", "hook_type": "number|contrarian|question|story|how-to",
               "format": "...", "pillar": "...", "alt_hook": "the runner-up first line", "sources": ["https://..."] } ] }
```

## visuals.json (Visual Designer)
A list of visual specs exactly as consumed by `render/render.mjs` (see the visual-design skill catalog).

## plan.json (assembled; the only file the pipeline reads)
```json
{
  "date": "2026-11-23",
  "status": "draft | approved | rejected",
  "topic_of_day": { ... },
  "visuals": [ ...visual specs... ],
  "posts": [
    { "id": "2026-11-23-li-1", "platform": "linkedin", "time_local": "08:30", "pillar": "signals", "format": "teardown",
      "hook_type": "number", "text": "...", "first_comment": "", "media": ["video-main"], "sources": ["https://..."], "alt_hook": "..." }
  ],
  "engagement_brief": ["..."],
  "review": { "editor": "brand-editor", "score": 9, "notes": "...", "checked_at": "ISO time" }
}
```
Rules the pipeline enforces (`scripts/validate_plan.py`): known platforms/templates/scenes, slots, X <= 280 chars and <= 2 hashtags, no links in LinkedIn/X bodies, LinkedIn <= 5 hashtags, stat posts need sources, no banned phrases, no repeated hooks, video 8-45 s, approved requires editor score >= `min_editor_score`.

## publish-result.json (written by the pipeline)
`scheduled` (with Buffer ids and dueAt), `skipped`, `errors`.
