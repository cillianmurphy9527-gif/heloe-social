// Shared helpers for cover.html and video.html. Loaded as a classic script.
(function () {
  function esc(s) {
    return String(s ?? "").replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  }
  // *word* -> <em>word</em> (accent highlight). Everything else is escaped.
  function rich(s) {
    return esc(s).replace(/\*(.+?)\*/g, "<em>$1</em>");
  }

  function applyBrand(brand, size, theme) {
    const [w, h] = size.split("x").map(Number);
    const u = Math.min(w, h) / 1080;
    const r = document.documentElement.style;
    const t = (brand.themes && brand.themes[theme || "dark"]) || brand.themes.dark;
    r.setProperty("--w", w + "px");
    r.setProperty("--h", h + "px");
    r.setProperty("--u", u);
    for (const k of ["bg", "surface", "surface2", "text", "muted", "accent", "glow", "grid"]) r.setProperty("--" + k, t[k]);
    r.setProperty("--brand", brand.palette.brand_indigo);
    r.setProperty("--font-display", `"${brand.fonts.display}"`);
    r.setProperty("--font-body", `"${brand.fonts.body}"`);
    r.setProperty("--font-mono", `"${brand.fonts.mono}"`);
    const canvas = document.querySelector(".canvas");
    canvas.className = "canvas theme-" + (theme || "dark") + (w > h * 1.2 ? " landscape" : " portrait");
    return { w, h, u };
  }

  function logoHTML(brand, theme) {
    const t = (brand.themes && brand.themes[theme || "dark"]) || {};
    const src = brand._logos && brand._logos[t.logo || "on_dark"];
    if (src) return `<div class="logo"><img src="${src}" alt=""></div>`;
    return `<div class="logo"><span class="wordmark">${esc(brand.name)}</span></div>`;
  }

  // Deterministic pseudo-random generator so renders are reproducible.
  function rng(seed) {
    let s = 0;
    for (const ch of String(seed)) s = (s * 31 + ch.charCodeAt(0)) >>> 0;
    return () => ((s = (s * 1664525 + 1013904223) >>> 0) / 4294967296);
  }

  // A "signal" line: calm baseline with one or two spikes (the moment something changes).
  function wavePath(seed, width, height, phase = 0) {
    const rand = rng(seed);
    const pts = [];
    const n = 120;
    const spikeAt = 0.62 + rand() * 0.12;
    for (let i = 0; i <= n; i++) {
      const x = i / n;
      let y = Math.sin((x * 9 + phase) * Math.PI) * 0.06 + Math.sin((x * 23 + phase * 1.7) * Math.PI) * 0.025;
      const d = x - spikeAt;
      y += Math.exp(-(d * d) / 0.0006) * -0.42 + Math.exp(-((d - 0.02) ** 2) / 0.0004) * 0.28;
      pts.push([x * width, height / 2 + y * height]);
    }
    return "M" + pts.map(p => p[0].toFixed(1) + " " + p[1].toFixed(1)).join(" L");
  }

  function waveSVG(seed, w, top, phase = 0) {
    const hh = 220;
    return `<svg class="bg-wave" style="top:${top}px" viewBox="0 0 ${w} ${hh}" preserveAspectRatio="none" width="${w}" height="${hh}">
      <path class="ghost" d="${wavePath(seed + "g", w, hh, phase + 0.5)}"/>
      <path d="${wavePath(seed, w, hh, phase)}"/></svg>`;
  }

  // Shrink an element's font-size until it fits its box (or reaches min scale).
  function fit(el, box, minScale = 0.5) {
    if (!el) return;
    const base = parseFloat(getComputedStyle(el).fontSize);
    let scale = 1;
    const tooBig = () => box.scrollHeight > box.clientHeight + 1 || el.scrollWidth > el.clientWidth + 1;
    while (tooBig() && scale > minScale) {
      scale -= 0.04;
      el.style.fontSize = base * scale + "px";
    }
  }

  // Split text into animatable word spans; *a b* marks emphasised words (can span several words).
  function wordsHTML(s) {
    const out = [];
    String(s || "").split(/(\*[^*]+\*)/).forEach(seg => {
      if (!seg) return;
      const em = /^\*[^*]+\*$/.test(seg);
      const txt = em ? seg.slice(1, -1) : seg;
      txt.split(/\s+/).filter(Boolean).forEach(w => out.push(`<span class="word">${em ? "<em>" + esc(w) + "</em>" : esc(w)}</span>`));
    });
    return out.join(" ");
  }

  window.H = { wordsHTML, esc, rich, applyBrand, logoHTML, rng, wavePath, waveSVG, fit };
})();
