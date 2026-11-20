---
name: social-copywriting
description: Writes Heloe's LinkedIn, X and Facebook post copy in the brand voice with platform-native structure, hooks and hashtags, producing content/DATE/copy.json. Use for "write the posts", "draft a LinkedIn post", "rewrite this tweet", "写文案", "改文案", or as the copywriting step of the daily content run.
---

# Social copywriting

Inputs: `REPO`, `D`, `content/D/brief.json` (slate), `content/D/scout.json` (facts and angles). Read `playbook/strategy.md` (voice, formats, hard rules), `playbook/platform-rules.md`, `playbook/hashtags.json`, the Active rules in `playbook/learnings.md`, and `playbook/founder-notes.md` for build-in-public slots.

## Process per slot
1. Read the slot's pillar, format and direction. Pull facts only from `scout.json` facts, the playbook or founder-notes.
2. Write two hooks (first lines) using different hook types (number, contrarian, question, story, how-to). Keep the stronger one; save the other as `alt_hook`.
3. Write the body in the slot's format (see strategy.md section 5 and `references/examples.md`).
4. Platform finish:
   - **LinkedIn**: 700-1,400 characters, hook in the first ~210 characters, one idea per line, ends with a question or takeaway, 3 hashtags at the end (1 broad + 1 niche + 1 pillar). No links in the body; when the post mentions Heloe or offers a resource, put `https://heloe.io/?utm_source=linkedin&utm_medium=social&utm_campaign=organic&utm_content=<post id>` in `first_comment` with one short sentence.
   - **X**: count characters (URLs count 23) and stay at or under 270 to leave margin. Line 1 stands alone. 0-1 hashtag. No links. Slot 3 is a genuine question that invites replies.
   - **Facebook**: 250-600 characters, conversational, may adapt the LinkedIn angle, 1-3 hashtags, may end with the UTM link (`utm_source=facebook`).
5. Product mentions: at most 1 post in 5 names Heloe. When it does, show the idea (a signal → the right moment → the right message), not a feature list.
6. Fill `sources` with every URL behind a number or claim in the text.

## Self-check before writing copy.json
- Read each post aloud in your head: would a busy founder stop scrolling at line 1?
- No banned phrases (strategy.md section 3), no "Excited to share", no rhetorical "Let that sink in", no emoji walls.
- Every number appears in `scout.json` facts with a URL.
- Nothing that sounds like a real customer, testimonial or result unless founder-notes says so.
- X length check, e.g. `python3 -c "import sys;print(len(sys.argv[1]))" "<text>"`.

## Output
Write `content/D/copy.json` (schema in the daily-content-run skill's `references/plan-schema.md`).
