#!/usr/bin/env node
// Render profile assets from the official brand kit: Facebook cover, X header, square avatar.
// Usage: node render/profile_assets.mjs [outDir=brand/social]
import { createRequire } from "module";
import fs from "fs";
import path from "path";
import { fileURLToPath, pathToFileURL } from "url";

const require = createRequire(import.meta.url);
const { chromium } = require("playwright");
const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const out = path.resolve(process.argv[2] || path.join(ROOT, "brand", "social"));
fs.mkdirSync(out, { recursive: true });

const brand = JSON.parse(fs.readFileSync(path.join(ROOT, "config", "brand.json"), "utf8"));
const uri = rel => `data:image/svg+xml;base64,${fs.readFileSync(path.join(ROOT, rel)).toString("base64")}`;
brand._logos = { on_dark: uri(brand.logo.on_dark), mark_white: uri("brand/mark-white.svg") };

const browser = await chromium.launch({ executablePath: process.env.CHROME_PATH || undefined, args: ["--allow-file-access-from-files"] });
const sizes = { "fb-cover": [1640, 624], "x-header": [1500, 500], "avatar": [1080, 1080] };
for (const [kind, [w, h]] of Object.entries(sizes)) {
  const page = await browser.newPage({ viewport: { width: w, height: h } });
  await page.goto(pathToFileURL(path.join(ROOT, "templates", "profile.html")).href);
  await page.evaluate(([k, b]) => window.renderProfile(k, b), [kind, brand]);
  await page.waitForFunction(() => window.__ready === true);
  await page.screenshot({ path: path.join(out, `heloe-${kind}.png`) });
  console.log("wrote", path.join(out, `heloe-${kind}.png`));
  await page.close();
}
await browser.close();
