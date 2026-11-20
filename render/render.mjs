#!/usr/bin/env node
// Render every visual in content/<date>/plan.json into docs/media/<date>/.
// Covers -> PNG, videos -> MP4 (H.264, silent) + poster JPG.
// Usage: node render/render.mjs --date 2026-11-23 [--only video-main] [--fps 30]
import { createRequire } from "module";
import { spawn } from "child_process";
import fs from "fs";
import path from "path";
import { fileURLToPath, pathToFileURL } from "url";

const require = createRequire(import.meta.url);
const { chromium } = require("playwright");

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const args = Object.fromEntries(process.argv.slice(2).reduce((a, v, i, arr) => (v.startsWith("--") ? a.concat([[v.slice(2), arr[i + 1] && !arr[i + 1].startsWith("--") ? arr[i + 1] : true]]) : a), []));

const date = args.date;
const planPath = args.plan || path.join(ROOT, "content", date, "plan.json");
if (!fs.existsSync(planPath)) { console.error("plan not found:", planPath); process.exit(1); }
const plan = JSON.parse(fs.readFileSync(planPath, "utf8"));
const outDir = args.out || path.join(ROOT, "docs", "media", plan.date || date);
fs.mkdirSync(outDir, { recursive: true });

const brand = JSON.parse(fs.readFileSync(path.join(ROOT, "config", "brand.json"), "utf8"));
function dataUri(rel) {
  if (!rel) return null;
  const p = path.join(ROOT, rel);
  if (!fs.existsSync(p)) return null;
  const ext = path.extname(p).slice(1).toLowerCase();
  const mime = ext === "svg" ? "image/svg+xml" : ext === "jpg" ? "image/jpeg" : `image/${ext}`;
  return `data:${mime};base64,${fs.readFileSync(p).toString("base64")}`;
}
brand._logos = {};
for (const [k, v] of Object.entries(brand.logo || {})) if (!k.startsWith("_")) brand._logos[k] = dataUri(v);

const fps = Number(args.fps || 30);
const browser = await chromium.launch({
  executablePath: process.env.CHROME_PATH || undefined,
  args: ["--allow-file-access-from-files", "--font-render-hinting=none"],
});

const manifestPath = path.join(outDir, "manifest.json");
const manifest = { date: plan.date, items: [] };
if (args.only && fs.existsSync(manifestPath)) {
  // partial re-render: keep entries for the other visuals
  manifest.items = JSON.parse(fs.readFileSync(manifestPath, "utf8")).items.filter(i => i.id !== args.only);
}
const visuals = (plan.visuals || []).filter(v => !args.only || v.id === args.only);

for (const v of visuals) {
  const [w, h] = (v.size || "1080x1350").split("x").map(Number);
  const page = await browser.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 1 });
  page.on("pageerror", e => console.error(`[${v.id}] page error:`, e.message));
  const t0 = Date.now();
  if (v.kind === "video") {
    await page.goto(pathToFileURL(path.join(ROOT, "templates", "video.html")).href);
    await page.evaluate(([s, b]) => window.initVideo(s, b), [v, brand]);
    await page.waitForFunction(() => window.__ready === true);
    const total = await page.evaluate(() => window.__total);
    const frames = Math.round(total * fps);
    const out = path.join(outDir, `${v.id}.mp4`);
    const ff = spawn("ffmpeg", ["-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", String(fps), "-i", "-",
      "-c:v", "libx264", "-preset", "veryfast", "-crf", "22", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
      "-vf", `scale=${w}:${h}`, out], { stdio: ["pipe", "inherit", "inherit"] });
    const done = new Promise((res, rej) => ff.on("close", c => (c === 0 ? res() : rej(new Error("ffmpeg exit " + c)))));
    for (let f = 0; f < frames; f++) {
      await page.evaluate(t => window.renderFrame(t), f / fps);
      const buf = await page.screenshot({ type: "jpeg", quality: 92 });
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once("drain", r));
    }
    ff.stdin.end();
    await done;
    // poster frame from the first scene once its text is in place
    await page.evaluate(t => window.renderFrame(t), Math.min(2.2, total - 0.1));
    await page.screenshot({ path: path.join(outDir, `${v.id}-poster.jpg`), type: "jpeg", quality: 90 });
    manifest.items.push({ id: v.id, kind: "video", file: `${v.id}.mp4`, poster: `${v.id}-poster.jpg`, seconds: total, size: v.size });
    console.log(`video ${v.id}: ${frames} frames, ${total}s, ${((Date.now() - t0) / 1000).toFixed(1)}s render`);
  } else {
    await page.goto(pathToFileURL(path.join(ROOT, "templates", "cover.html")).href);
    await page.evaluate(([s, b]) => window.renderCover(s, b), [v, brand]);
    await page.waitForFunction(() => window.__ready === true);
    const overflow = await page.evaluate(() => window.__overflow);
    const out = path.join(outDir, `${v.id}.png`);
    await page.screenshot({ path: out, type: "png" });
    manifest.items.push({ id: v.id, kind: "cover", file: `${v.id}.png`, size: v.size, overflow });
    console.log(`cover ${v.id}${overflow ? " (WARNING: text overflow)" : ""}: ${((Date.now() - t0) / 1000).toFixed(1)}s`);
  }
  await page.close();
}
await browser.close();
fs.writeFileSync(manifestPath, JSON.stringify(manifest, null, 2));
const overflowing = manifest.items.filter(i => i.overflow);
if (overflowing.length) { console.error("Overflow in:", overflowing.map(i => i.id).join(", ")); process.exitCode = 2; }
