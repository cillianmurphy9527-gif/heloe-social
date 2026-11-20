#!/usr/bin/env python3
"""Discover the Buffer organization and the LinkedIn / X / Facebook channel ids; write them into config/channels.json.
Also prints the createPost input schema so field changes on Buffer's side are visible in the Actions log."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from buffer import gql

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SERVICE_MAP = {"linkedin": "linkedin", "twitter": "x", "x": "x", "facebook": "facebook"}


def main():
    orgs = gql("query { account { organizations { id name } } }")["account"]["organizations"]
    print("organizations:", orgs)
    cfg_path = os.path.join(ROOT, "config", "channels.json")
    cfg = json.load(open(cfg_path))
    org = orgs[0]
    cfg["buffer_organization_id"] = org["id"]
    chans = gql("query($o: OrganizationId!) { channels(input: {organizationId: $o}) { id name service } }",
                {"o": org["id"]})["channels"]
    print("channels:", json.dumps(chans, indent=1))
    found = {}
    for c in chans:
        key = SERVICE_MAP.get(str(c["service"]).lower())
        if key and key in cfg["channels"] and key not in found:
            cfg["channels"][key]["buffer_channel_id"] = c["id"]
            cfg["channels"][key]["buffer_name"] = c["name"]
            found[key] = c["name"]
    json.dump(cfg, open(cfg_path, "w"), indent=2, ensure_ascii=False)
    print("mapped:", found)
    missing = [k for k in cfg["channels"] if k not in found]
    if missing:
        print("WARNING: no Buffer channel found for", missing)
    for t in ["CreatePostInput", "LinkedInPostMetadataInput", "FacebookPostMetadataInput", "TwitterPostMetadataInput"]:
        try:
            r = gql('query($n: String!) { __type(name: $n) { inputFields { name type { name kind ofType { name kind } } } } }', {"n": t})
            print(t, [f["name"] for f in (r["__type"] or {}).get("inputFields", [])])
        except Exception as e:
            print("introspection skipped:", e)
            break


if __name__ == "__main__":
    main()
