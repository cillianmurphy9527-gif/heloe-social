# heloe-social-ops

Multi-agent social media operations for Heloe (heloe.io). The plugin holds the roles and methods; the `heloe-social` GitHub repo holds the state (playbook, plans, media, metrics) and the GitHub Actions pipeline that publishes through Buffer.

## Roles (agents)
| Agent | Job |
|---|---|
| trend-scout | Finds and scores today's topics (Hacker News, Google News, Product Hunt, Reddit scan, web search) |
| copywriter | Writes LinkedIn / X / Facebook copy in the brand voice |
| visual-designer | Designs and renders covers (PNG) and motion videos (MP4), checks them visually |
| brand-editor | Independent pre-publish gate: facts, safety, voice, platform rules, visuals |
| growth-analyst | Weekly performance analysis and playbook updates |

## Skills
| Skill | Trigger |
|---|---|
| daily-content-run | Editor-in-Chief orchestration of the whole day (scheduled daily) |
| trend-scouting, social-copywriting, visual-design, brand-review | Methods used by the agents; also usable on their own |
| weekly-review | Monday retrospective (scheduled weekly) |
| reddit-scan | Reads Reddit through the founder's Chrome (scheduled, needs the computer) |
| social-ops-control | Pause/resume, status, edit/delete a post, change times, brand updates |

## Connections
- GitHub (claude.ai built-in integration) with push access to `cillianmurphy9527-gif/heloe-social`. The repo hosts media on GitHub Pages and runs trend collection in GitHub Actions.
- Buffer connector (`https://mcp.buffer.com/mcp`): Claude schedules posts with `create_post`, reads metrics with `list_posts` / `get_aggregated_post_metrics`.
- Product Hunt connector (optional, for trend scouting).
- Claude in Chrome (optional, for the Reddit scan).

## Approval rule
Posts that carry a video are sent to the founder first and scheduled only after an explicit OK. Text and image posts publish automatically once the Brand Editor approves them (score >= 8).
