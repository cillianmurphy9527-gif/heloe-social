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
- GitHub (claude.ai connector) with push access to `<owner>/heloe-social`.
- Buffer MCP (`https://mcp.buffer.com/mcp`, OAuth): read queue and metrics, edit or delete a post. Publishing itself runs in GitHub Actions with the `BUFFER_API_KEY` repo secret.
- Product Hunt connector (optional, for trend scouting).
- Claude in Chrome (optional, for the Reddit scan).
