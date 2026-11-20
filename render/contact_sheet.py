#!/usr/bin/env python3
"""Make one QA image of a day's renders (covers + 6 frames per video) for visual review.
Usage: python3 render/contact_sheet.py 2026-11-23 [/tmp/qa-2026-11-23.png]"""
import json, os, subprocess, sys, tempfile
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = sys.argv[1]
out = sys.argv[2] if len(sys.argv) > 2 else f"/tmp/qa-{d}.png"
media = os.path.join(ROOT, "docs", "media", d)
items = json.load(open(os.path.join(media, "manifest.json")))["items"]
tiles, H = [], 420
for it in items:
    if it["kind"] == "cover":
        im = Image.open(os.path.join(media, it["file"])).convert("RGB")
        tiles.append(im.resize((int(im.width * H / im.height), H)))
    else:
        secs = it["seconds"]
        for k in range(6):
            t = secs * (k + 0.6) / 6.2
            fd, tmp = tempfile.mkstemp(suffix=".jpg"); os.close(fd)
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", f"{t:.2f}", "-i", os.path.join(media, it["file"]),
                            "-frames:v", "1", tmp], check=True)
            im = Image.open(tmp).convert("RGB")
            tiles.append(im.resize((int(im.width * H / im.height), H)))
            os.remove(tmp)
row_w = 2400
rows, cur, w = [], [], 0
for t in tiles:
    if w + t.width > row_w and cur:
        rows.append(cur); cur, w = [], 0
    cur.append(t); w += t.width + 8
rows.append(cur)
sheet = Image.new("RGB", (row_w, len(rows) * (H + 8)), (50, 50, 50))
for r, row in enumerate(rows):
    x = 0
    for t in row:
        sheet.paste(t, (x, r * (H + 8))); x += t.width + 8
sheet.save(out)
print(out)
