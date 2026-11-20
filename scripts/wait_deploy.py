#!/usr/bin/env python3
"""Wait until the 'Render and publish' workflow for a commit has deployed media to GitHub Pages.
Uses the public GitHub API (no token needed for a public repo).

Usage: python3 scripts/wait_deploy.py <commit-sha> [timeout_seconds=900]
Exit 0 when the workflow run for that commit concluded with success; 1 on failure or timeout.
"""
import json, os, sys, time, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
repo = json.load(open(os.path.join(ROOT, "config", "settings.json")))["repo"]
sha, timeout = sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 900
url = f"https://api.github.com/repos/{repo}/actions/runs?head_sha={sha}&per_page=20"
t0 = time.time()
while time.time() - t0 < timeout:
    try:
        req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json", "User-Agent": "heloe-social"})
        runs = json.loads(urllib.request.urlopen(req, timeout=30).read()).get("workflow_runs", [])
    except Exception as e:
        print("api error:", e)
        runs = []
    run = next((r for r in runs if r.get("name") == "Render and publish"), None)
    if run:
        print(f"{run['status']} {run.get('conclusion')} {run['html_url']}")
        if run["status"] == "completed":
            sys.exit(0 if run.get("conclusion") == "success" else 1)
    else:
        print("waiting for the workflow to start...")
    time.sleep(20)
print("timeout")
sys.exit(1)
