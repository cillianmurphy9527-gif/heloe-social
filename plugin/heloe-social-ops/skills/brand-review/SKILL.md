---
name: brand-review
description: Independent pre-publish review of a day's Heloe social plan: fact-checks numbers against sources, checks brand voice, platform rules, duplicates, safety and the rendered visuals, and writes content/<date>/review.json with approve / revise / drop verdicts and a 1-10 score. Use for "review today's posts", "check this before it goes out", "审核", or as the review step of the daily content run.
---

# Brand review

Inputs: `REPO`, `D`. Read `content/D/plan.json`, `content/D/scout.json`, `playbook/strategy.md` (sections 3 and 8 especially), `playbook/platform-rules.md`, `playbook/founder-notes.md`, and the last 30 days of `data/posts.jsonl`.

## Checks (in this order)
1. **Mechanical**: run `python3 scripts/validate_plan.py D`. Every error is at least a `revise`.
2. **Facts**: for every number, date, product claim or news claim in post text and in visual fields, open the cited source (`WebFetch`) and confirm it says that. Unverifiable → `revise` (remove or soften the claim) or `drop` if the post depends on it. Mismatched number → `revise` with the correct figure.
3. **No fabrication**: no invented customers, results, testimonials, quotes attributed to real people, or private company data. Build-in-public claims must appear in founder-notes. Signal-card companies must be generic unless named in a sourced news story.
4. **Safety and taste**: nothing that exploits tragedy, layoffs of named people, politics, or mocks individuals; no competitor bashing by name; no guarantees ("guaranteed replies", "100% inbox"). Reddit content is paraphrased with no usernames and no long verbatim quotes.
5. **Voice**: practitioner tone, specific, no banned phrases, no hype, product named in at most 1 in 5 posts.
6. **Platform fit**: hook strength in line 1, LinkedIn see-more cut, X length and standalone readability, hashtag counts, link placement.
7. **Duplicates**: hook or angle too close to anything in the last 30 days.
8. **Visuals**: run `python3 render/contact_sheet.py D /tmp/review-D.png` and read the image. Check typos, overflow, wrong numbers, unreadable contrast, highlight on the wrong word, and that each visual matches its post.

## Verdicts
- `approve`: ready as is.
- `revise`: give the exact replacement (full new `text`, or the exact field and new value for a visual). Small, surgical fixes.
- `drop`: unfixable (false premise, unsafe, duplicate).

Score the day 1-10: 9-10 = strong and safe; 8 = publishable; <=7 = do not publish without changes. Any unresolved factual or safety problem caps the score at 6.

## Output: content/D/review.json
```json
{ "date": "D", "score": 8, "summary": "one line", "checked_at": "ISO time",
  "posts": [ { "id": "...", "verdict": "approve|revise|drop", "issues": ["..."], "fix": { "text": "full replacement text" } } ],
  "visuals": [ { "id": "...", "verdict": "approve|revise", "issues": ["..."], "fix": { "fields.caption": "new value" } } ] }
```
Do not edit plan.json yourself.
