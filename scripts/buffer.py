"""Minimal Buffer GraphQL client (https://developers.buffer.com). Needs env BUFFER_API_KEY."""
import json, os, random, time, urllib.error, urllib.request

ENDPOINT = "https://api.buffer.com"


class BufferError(Exception):
    pass


def gql(query, variables=None, max_wait=120):
    key = os.environ.get("BUFFER_API_KEY")
    if not key:
        raise BufferError("BUFFER_API_KEY is not set (add it under GitHub repo Settings > Secrets and variables > Actions)")
    body = json.dumps({"query": query, "variables": variables or {}}).encode()
    for attempt in range(4):
        req = urllib.request.Request(ENDPOINT, data=body, method="POST", headers={
            "Content-Type": "application/json", "Authorization": f"Bearer {key}",
            "User-Agent": "heloe-social/1.0"})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                data = json.loads(r.read())
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 3:
                wait = min(max_wait, int(e.headers.get("Retry-After", "30")))
                print(f"[buffer] rate limited, waiting {wait}s")
                time.sleep(wait + random.random())
                continue
            raise BufferError(f"HTTP {e.code}: {e.read().decode()[:500]}")
        if data.get("errors"):
            raise BufferError(json.dumps(data["errors"])[:800])
        return data["data"]
    raise BufferError("gave up after retries")
