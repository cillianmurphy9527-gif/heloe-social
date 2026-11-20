#!/usr/bin/env python3
"""Deterministic checks on content/<date>/plan.json. Used by the Brand Editor agent before commit
and by the publish workflow before anything goes to Buffer.

Usage: python scripts/validate_plan.py 2026-11-23 [--json]
Exit code 0 = no errors (warnings allowed), 1 = errors.
"""
import json, os, re, sys, difflib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BANNED = ["game-changer", "game changer", "revolutionize", "revolutionise", "unlock", "supercharge", "fast-paced world",
          "leverage", "synergy", "in today's", "delve", "elevate your", "seamlessly", "cutting-edge", "best-in-class"]
URL_RE = re.compile(r"https?://\S+|\b[\w-]+\.(?:io|com|ai|co|net|org)\b(?:/\S*)?", re.I)
TEMPLATES = {"headline", "stat", "list", "quote", "signal"}
SCENES = {"hook", "stat", "list", "quote", "signal", "cta"}
PLATFORMS = {"linkedin", "x", "facebook"}
DAYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]


def x_length(text):
    # X counts every URL as 23 characters
    return len(URL_RE.sub("x" * 23, text))


def load_history(exclude_date):
    path = os.path.join(ROOT, "data", "posts.jsonl")
    out = []
    if os.path.exists(path):
        for line in open(path):
            try:
                r = json.loads(line)
                if r.get("date") != exclude_date:
                    out.append(r)
            except ValueError:
                pass
    return out[-300:]


def validate(date):
    errors, warnings = [], []
    p = os.path.join(ROOT, "content", date, "plan.json")
    if not os.path.exists(p):
        return [f"missing {p}"], []
    try:
        plan = json.load(open(p))
    except ValueError as e:
        return [f"plan.json is not valid JSON: {e}"], []

    settings = json.load(open(os.path.join(ROOT, "config", "settings.json")))
    channels = json.load(open(os.path.join(ROOT, "config", "channels.json")))["channels"]
    hashtags = json.load(open(os.path.join(ROOT, "playbook", "hashtags.json")))

    if plan.get("date") != date:
        errors.append(f"plan.date {plan.get('date')} != folder {date}")
    if plan.get("status") not in ("approved", "draft", "rejected"):
        errors.append("status must be approved | draft | rejected")
    rv = plan.get("review") or {}
    if plan.get("status") == "approved" and (rv.get("score") or 0) < settings.get("min_editor_score", 8):
        errors.append(f"approved but editor score {rv.get('score')} < {settings.get('min_editor_score')}")

    vids = {}
    for v in plan.get("visuals", []):
        vids[v.get("id")] = v
        if v.get("kind") == "cover" and v.get("template") not in TEMPLATES:
            errors.append(f"visual {v.get('id')}: unknown template {v.get('template')}")
        if v.get("kind") == "video":
            sc = v.get("scenes") or []
            total = sum(float(s.get("duration", 0)) for s in sc)
            if not 8 <= total <= 45:
                errors.append(f"video {v['id']}: total {total:.1f}s outside 8-45s")
            for s in sc:
                if s.get("type") not in SCENES:
                    errors.append(f"video {v['id']}: unknown scene {s.get('type')}")
            if sc and sc[-1].get("type") != "cta":
                warnings.append(f"video {v['id']}: last scene should be cta")
        if not re.fullmatch(r"\d{3,4}x\d{3,4}", str(v.get("size", ""))):
            errors.append(f"visual {v.get('id')}: bad size {v.get('size')}")

    weekday = None
    try:
        import datetime as dt
        weekday = DAYS[dt.date.fromisoformat(date).weekday()]
    except ValueError:
        errors.append("bad date")

    history = load_history(date)
    hist_hooks = [(h.get("text") or "").split("\n")[0].lower() for h in history]
    per_platform = {}
    ids = set()
    for post in plan.get("posts", []):
        pid, plat, text = post.get("id"), post.get("platform"), post.get("text") or ""
        tag = f"post {pid}"
        if pid in ids:
            errors.append(f"{tag}: duplicate id")
        ids.add(pid)
        if plat not in PLATFORMS:
            errors.append(f"{tag}: unknown platform {plat}")
            continue
        per_platform[plat] = per_platform.get(plat, 0) + 1
        if not re.fullmatch(r"\d{2}:\d{2}", str(post.get("time_local", ""))):
            errors.append(f"{tag}: time_local must be HH:MM")
        elif weekday and post["time_local"] not in channels[plat]["slots"].get(weekday, []):
            warnings.append(f"{tag}: {post['time_local']} is not a configured {plat} slot for {weekday}")
        for m in post.get("media", []):
            if m not in vids:
                errors.append(f"{tag}: media {m} not in visuals")
        low = text.lower()
        for b in BANNED:
            if b in low:
                errors.append(f"{tag}: banned phrase '{b}'")
        tags = re.findall(r"(?<!\w)#\w+", text)
        for t in tags:
            if t in hashtags.get("avoid", []):
                errors.append(f"{tag}: avoided hashtag {t}")
        if re.search(r"\b(?:lorem|TODO|TBD|\[insert)", text, re.I):
            errors.append(f"{tag}: placeholder text left in")
        if plat == "x":
            n = x_length(text)
            if n > 280:
                errors.append(f"{tag}: X post is {n} chars (max 280)")
            if len(tags) > 2:
                errors.append(f"{tag}: {len(tags)} hashtags on X (max 2)")
            if URL_RE.search(text):
                warnings.append(f"{tag}: link in X post body reduces reach")
        if plat == "linkedin":
            if not 300 <= len(text) <= 3000:
                warnings.append(f"{tag}: LinkedIn length {len(text)} (target 700-1400)")
            if len(tags) > 5:
                errors.append(f"{tag}: {len(tags)} hashtags on LinkedIn (max 5)")
            if URL_RE.search(text):
                errors.append(f"{tag}: link in LinkedIn body; move it to first_comment")
        if plat == "facebook" and len(text) > 2000:
            warnings.append(f"{tag}: Facebook post is long ({len(text)})")
        if post.get("format") in ("stat", "data") and not post.get("sources"):
            errors.append(f"{tag}: stat post without sources")
        hook = text.split("\n")[0].lower()
        for old in hist_hooks:
            if hook and difflib.SequenceMatcher(None, hook, old).ratio() > 0.85:
                errors.append(f"{tag}: hook repeats a recent post: '{old[:60]}'")
                break

    caps = settings.get("max_posts_per_day", {})
    for plat, n in per_platform.items():
        if n > caps.get(plat, 99):
            errors.append(f"{plat}: {n} posts > daily cap {caps.get(plat)}")
    return errors, warnings


if __name__ == "__main__":
    date = sys.argv[1]
    errs, warns = validate(date)
    if "--json" in sys.argv:
        print(json.dumps({"errors": errs, "warnings": warns}, indent=1))
    else:
        for w in warns:
            print("WARN ", w)
        for e in errs:
            print("ERROR", e)
        print(f"{len(errs)} errors, {len(warns)} warnings")
    sys.exit(1 if errs else 0)
