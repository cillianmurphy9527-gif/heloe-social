#!/usr/bin/env bash
# Render the sample plan into /tmp/heloe-render-test to check templates after brand changes.
set -euo pipefail
cd "$(dirname "$0")/.."
OUT=/tmp/heloe-render-test
rm -rf "$OUT"; mkdir -p "$OUT"
if [ ! -d node_modules/playwright ]; then export NODE_PATH="${NODE_PATH:-$(npm root -g 2>/dev/null)}"; [ -d /opt/npm-tools/node_modules/playwright ] && export NODE_PATH=/opt/npm-tools/node_modules; fi
[ -z "${CHROME_PATH:-}" ] && [ -x /usr/bin/google-chrome ] && export CHROME_PATH=/usr/bin/google-chrome
node render/render.mjs --plan examples/sample-plan.json --out "$OUT" "$@"
echo "rendered into $OUT"
