# Heloe Social Strategy (agent-facing source of truth)

## 1. Positioning
- **Brand label:** Heloe is the outbound platform that is *excellent at dynamic sales signals*. Like Apollo = database, Hunter = email finding, ZeroBounce = verification, **Heloe = know when to reach out**.
- **Secondary benefit (never the headline):** one-stop outbound — domains, mailboxes, warmup and monitoring, lead search, verified contacts — so teams stop juggling five tools.
- **Working line:** "Sell on signals, not static lists." (founder may replace it in `config/brand.json`)
- **What signals are:** fresh, verified changes at a target company — funding, hiring needs, deals, business changes, org/leadership changes, public news — checked at the moment of search, with AI advice on whether, how and when to reach out.

## 2. Audience (who we write for)
1. Founders running founder-led sales at B2B startups and SMBs (primary).
2. SDRs/BDRs and AEs who own their own pipeline.
3. Sales leaders, RevOps and growth people choosing outbound tooling.
4. Agencies running outbound for clients.
Regions: US first, then UK/EU/ANZ. Write in clear US English.

**What they care about:** replies and meetings, not "AI". Deliverability scares them. They are tired of generic AI spam and of lists that went stale.

## 3. Voice
- Practitioner, not marketer. Sounds like a sharp founder who has run outbound, not a brand account.
- Specific > clever. Concrete examples, numbers with sources, real-sounding scenarios.
- Short sentences. One idea per line on LinkedIn. No corporate filler.
- Confident but never hypey. No "game-changer", "revolutionize", "unlock", "supercharge", "in today's fast-paced world", "leverage", emoji walls.
- Product mentions are rare: at most 1 in 5 posts names Heloe directly; when it does, show the concept (signals → timing) rather than a feature dump.
- We criticize practices (spray-and-pray, stale lists), never competitors by name.

## 4. Pillars
See `config/pillars.json`. Every post belongs to exactly one pillar and one format.

## 5. Formats library
| Format | Shape | Best on |
|---|---|---|
| hot-take | bold claim in line 1, 3-5 lines of reasoning, a question | X, LinkedIn |
| stat | one number, what it means, what to do about it, source | all |
| teardown | a trigger (e.g., "Company raised Series A") -> the message we'd send -> why it works | LinkedIn |
| listicle | "5 signals that mean..." numbered, each 1 line | LinkedIn, FB |
| story | short scenario with a turn and a lesson | LinkedIn |
| myth-fact | "Myth: ... / Fact: ..." | X, LinkedIn |
| checklist | setup steps, copy-saveable | LinkedIn, FB |
| question | genuine question to the community, one line of context | X |

## 6. Cold start: first 30 days
Accounts start at zero. Distribution comes from consistency, format testing, and human engagement — not from volume alone.

**Week 0 (before automation turns on)**
- Profiles complete on all 3 platforms: name, bio with the brand label, banner, link to heloe.io with UTM, a pinned intro post.
- Seed 3 evergreen posts per platform so a visitor sees substance.

**Weeks 1-2: find the voice (exploration)**
- Cadence: LinkedIn 1/weekday, X 3/day (2 on weekends), Facebook 1/weekday + Sat.
- Rotate every format at least twice per platform. Vary hook styles (number, contrarian, question, story).
- Log every post with pillar, format, hook type, media type in `data/posts.jsonl`.
- Human engagement: 15-20 minutes a day by the founder (comments on posts by people in the audience). The daily run produces an "engagement brief" with comment ideas; automated replies are not used because platform rules forbid them.

**Weeks 3-4: double down (exploitation)**
- Rank formats and pillars by engagement rate (engagements / impressions) per platform, not by raw likes.
- Cut the bottom 30% of formats; give their slots to the top performers.
- Launch 1-2 recurring series from the winners (e.g., "Signal of the Day", "Deliverability Friday").
- Start LinkedIn document carousels if image posts outperform text.

**30-day targets (realistic for zero start, review weekly)**
- LinkedIn: engagement rate >= 2.5%, 100-300 followers (personal profiles grow faster than company pages).
- X: engagement rate >= 1%, 100-200 followers, at least 1 post > 2,000 impressions.
- Facebook: treat as secondary; engagement rate >= 1%.
- Every week: impressions trend up week over week.

## 7. Decision rules (the analyst updates these in learnings.md)
- Judge a format only after >= 5 posts of it on that platform.
- Change one variable at a time when running an experiment.
- If a post beats the 14-day median engagement rate by 2x, schedule a follow-up on the same angle within 3 days.
- If a platform's 7-day impressions fall 30% week over week, the analyst investigates timing, format mix and hook quality before changing volume.

## 8. Hard rules
- Never invent statistics, quotes, customers, results or company facts. Every number has a source URL in the plan.
- Never quote Reddit users verbatim or name them; paraphrase community sentiment ("founders on r/sales are debating...").
- Never post about tragedies, politics, layoffs of named individuals, or anything that reads as exploiting bad news.
- No external links in LinkedIn or X post bodies; put the link in the LinkedIn first comment. Facebook may include the UTM link.
- Build-in-public posts use only facts written in `playbook/founder-notes.md`.
