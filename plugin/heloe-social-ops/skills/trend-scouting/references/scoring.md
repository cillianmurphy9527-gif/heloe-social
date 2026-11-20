# Topic scoring rubric (0-10 each)

total = 0.30 * heat + 0.30 * relevance + 0.25 * bridge + 0.15 * freshness

## heat — how much attention right now
- 9-10: Reddit post with 300+ comments in the niche subs, HN front page with 300+ points, or covered by 5+ outlets today
- 7-8: Reddit 100+ comments, HN 100+ points, 3+ outlets, or Product Hunt top 5 in a relevant category
- 4-6: one solid outlet or a mid-size discussion
- 0-3: barely discussed

## relevance — does Heloe's audience care
- 9-10: directly about outbound, cold email, prospecting, sales tooling, deliverability, sales hiring
- 6-8: founders/GTM/SaaS growth broadly, AI in sales, funding climate
- 3-5: general tech/business with an indirect sales angle
- 0-2: off-audience

## bridge — can we connect it to Heloe's label (signals, timing, knowing when to reach out) without forcing it
- 9-10: the topic is itself about timing, triggers, intent, stale data or spray-and-pray failing
- 6-8: a natural one-sentence bridge exists ("this funding wave = a signal-rich month for sellers")
- 3-5: only a generic outbound lesson
- 0-2: forced

## freshness
- 10: last 24h; 8: 24-48h; 5: this week; 2: older (evergreen only)

## Tie-breakers
1. A topic not used in the last 14 days of `data/posts.jsonl`
2. A topic with a hard number from a credible source (feeds the stat format)
3. A topic that suits video (clear before/after, a list, a number that animates well)
