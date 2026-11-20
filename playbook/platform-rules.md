# Platform rules

## LinkedIn (founder's personal profile)
- First person, founder voice. One personal angle per post ("Here's what I'm seeing...", "We learned this building Heloe...") but never invented experiences: personal claims come only from founder-notes.md.
- Length 700-1,400 characters. The first 2 lines (~210 characters) decide whether people click "see more": open with the hook, no greeting, no hashtags up top.
- One sentence per line, blank line between ideas. Max 1 emoji per post, often 0.
- End with a question or a clear takeaway.
- 3 hashtags at the very end, from `hashtags.json` (1 broad, 1 niche, 1 pillar).
- No links in the body. Put the heloe.io UTM link in `first_comment` only when the post mentions Heloe or a resource.
- Media: 1080x1350 (4:5) image, or the day's cinematic 16:9 video (matches the launch video). Videos are sent to the founder for approval before scheduling.

## X (Twitter)
- Hard limit 280 characters (count URLs as 23). Aim for 120-240.
- Line 1 must stand alone as the hook. Prefer concrete claims and numbers.
- 0-1 hashtag, never more than 2. No links.
- Text-only posts are fine and often perform best; media posts use a 1600x900 (16:9) cover or the 16:9 video.
- Questions and replies drive growth; slot 3 is reserved for a reply-inviting question.

## Facebook (Page)
- Length 250-600 characters, conversational, can be a lightly adapted version of the day's LinkedIn post.
- 1-3 hashtags. The UTM link to heloe.io is allowed at the end.
- Media: reuse the day's 1080x1350 cover or the 16:9 video. Post type: `post`.

## Universal
- US English, American spelling.
- Each post must be understandable without the image.
- No duplicate hooks within 30 days (the editor checks `data/posts.jsonl`).
- Avoid banned phrases listed in `strategy.md` section 3.
