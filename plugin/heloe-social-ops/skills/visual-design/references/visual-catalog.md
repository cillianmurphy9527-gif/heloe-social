# Visual catalog (what render/render.mjs understands)

All visuals share: `id` (kebab-case), `kind` (`cover` | `video`), `size` (`WIDTHxHEIGHT`), `theme` (`dark` | `light` | `accent`). Brand colors, fonts and logo come from `config/brand.json` automatically. `*text*` highlights words in the accent color.

## Covers (`kind: "cover"`)
| template | fields | use for |
|---|---|---|
| `headline` | `kicker`, `headline`, `sub` (optional) | hot takes, myths, story hooks |
| `stat` | `kicker`, `stat` (string, e.g. "3.43%"), `caption`, `source` | one strong number |
| `list` | `kicker`, `title`, `items` (3-6 strings) | listicles, checklists |
| `quote` | `kicker`, `quote`, `attribution` | community pulse, a principle (attribution like "The r/sales consensus this week", never a username or invented person) |
| `signal` | `kicker`, `headline`, `signal_type`, `company`, `detail`, `advice`, `when` (optional) | signal teardowns, "signal of the day" |
Optional on any cover: `footer` (replaces the domain at bottom right), `wave: false` to hide the signal line.

Example:
```json
{ "id": "cover-li", "kind": "cover", "template": "stat", "size": "1080x1350", "theme": "dark",
  "fields": { "kicker": "Outbound benchmark 2026", "stat": "3.43%", "caption": "Average cold email reply rate. Down from *5%* a year ago.", "source": "Cleverly, May 2026" } }
```

## Videos (`kind: "video"`)
Fields: `label` (top-right text, e.g. the pillar name), `scenes` (list). Rendered at 30 fps, silent, H.264, with a progress bar and scene counter.

| scene `type` | fields | motion |
|---|---|---|
| `hook` | `kicker` (optional), `text` | words pop in one by one |
| `stat` | `kicker`, `value` (number), `decimals`, `prefix`, `suffix`, `label`, `source` | number counts up |
| `list` | `title`, `items` (max 5) | items reveal in sequence |
| `quote` | `text`, `attribution` | quote mark pops, text fades in |
| `signal` | `headline` (optional), `signal`, `company`, `detail`, `advice`, `when` | radar pulse, card slides in, advice types out |
| `cta` | `text` (defaults to brand tagline), `url` (defaults to domain) | logo scales in, tagline reveals |
Every scene needs `duration` in seconds.

Example:
```json
{ "id": "video-main", "kind": "video", "size": "1080x1350", "theme": "dark", "label": "Signal selling",
  "scenes": [
    { "type": "hook", "duration": 3.2, "kicker": "Outbound in 2026", "text": "Cold email isn't dead. *Bad timing* is." },
    { "type": "stat", "duration": 4.0, "kicker": "Average reply rate", "value": 3.43, "decimals": 2, "suffix": "%", "label": "Down from *5%* last year.", "source": "Cleverly, May 2026" },
    { "type": "list", "duration": 5.5, "title": "What changed?", "items": ["Inboxes are saturated", "Spam filters got stricter", "Lists go stale in weeks"] },
    { "type": "signal", "duration": 5.5, "headline": "Reach out when *something changes*", "signal": "Funding", "company": "Series A · B2B fintech · 45 people", "detail": "Raised $12M yesterday. Hiring 4 AEs.", "advice": "Message the VP Sales this week. Angle: ramping new AEs fast." },
    { "type": "cta", "duration": 3.0, "text": "Sell on signals, not static lists.", "url": "heloe.io" }
  ] }
```
