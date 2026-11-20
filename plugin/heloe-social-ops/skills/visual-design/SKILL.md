---
name: visual-design
description: Designs, renders and visually checks Heloe's branded social covers (PNG) and motion-graphic videos (MP4) from the repo's HTML templates, producing content/DATE/visuals.json and files in docs/media/DATE/. Use for "make the cover", "make today's video", "redo this image", "做封面", "做视频", or as the design step of the daily content run.
---

# Visual design

Inputs: `REPO`, `D`, `content/D/brief.json` (`media_plan`, slate), `content/D/scout.json` (facts). Read `references/visual-catalog.md` for every template, scene type and field.

## 1. Design the specs
For each item in `media_plan`:
- Pick the template or scene sequence that fits the post format (stat → `stat`; listicle/checklist → `list`; hot take → `headline` or `quote`; signal teardown → `signal`).
- Write very little text: headline <= 10 words, list items <= 6 words, captions <= 14 words. The post carries the detail; the visual stops the scroll.
- Use `*asterisks*` around 1-3 words to highlight them in the accent color. One highlight per visual.
- Every number on a visual must come from `scout.json` facts and carry a short `source` line (publisher + month).
- Signal cards use generic company descriptors ("Series A · B2B fintech · 45 people") unless the company is named in a sourced news item. Never invent a real company's data.
- Rotate themes: avoid using the same theme as the previous day's main asset (check `content/<D-1>/plan.json`). `dark` is the default; use `light` or `accent` for contrast about 1 day in 3.
- Videos match the founder's launch video (2026-11-19): `theme: "cinematic"`, `size: "1920x1080"`, open with a `logo3d` scene (2.4-2.8 s, the glossy 3D H mark), 2-4 content scenes, close with a `logo3d` scene carrying the brand line ("Know who. Know when. Know why. Know how.") and `url: "heloe.io"`. Total 15-25 s. The first content scene is a `hook` that reads in under 2 s. Scene durations: logo3d intro 2.4-2.8, hook 2.8-3.5, stat 3.5-4.5, list 1.4 s per item + 1.5, quote 3.5-4.5, signal 5-6, logo3d outro 3.5-4.
- Sizes: covers `1080x1350` for LinkedIn/Facebook and `1600x900` for X; videos `1920x1080`. The founder approves every video before it is scheduled, so its quality bar is the launch video.

Write the list to `content/D/visuals.json`.

## 2. Render
Copy the specs into a temporary `content/D/plan.json` (`{"date": D, "status": "draft", "visuals": [...], "posts": []}`) if the editor has not assembled one yet, then:
```bash
cd REPO && render/render.sh D            # all visuals
render/render.sh D --only <visual-id>    # one visual after a fix
python3 render/contact_sheet.py D /tmp/qa-D.png
```
The renderer prints `WARNING: text overflow` when text was too long to fit.

## 3. Look at the result
Open `/tmp/qa-D.png` with the Read tool and check: no overflow or clipped text, nothing awkwardly wrapped (a single orphan word on the last line), highlights land on the key words, numbers are correct, contrast is readable, the video's hook frame makes sense on its own. Fix and re-render, at most 2 rounds. If a video still fails, fall back to a cover for that slot and say so.

## 4. Hand back
Reply with each visual id, file name, and one line describing it. Do not commit; the Editor-in-Chief commits everything together.
