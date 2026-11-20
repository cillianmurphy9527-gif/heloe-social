#!/usr/bin/env bash
# Portable wrapper: finds playwright + a Chrome binary in Claude sessions or CI, then renders.
# Usage: render/render.sh <date> [--only <visual-id>]
set -euo pipefail
cd "$(dirname "$0")/.."
if [ ! -d node_modules/playwright ]; then
  export NODE_PATH="${NODE_PATH:-$(npm root -g 2>/dev/null)}"
  [ -d /opt/npm-tools/node_modules/playwright ] && export NODE_PATH=/opt/npm-tools/node_modules
fi
if [ -z "${CHROME_PATH:-}" ]; then
  for c in /usr/bin/google-chrome /usr/bin/chromium /usr/bin/chromium-browser; do [ -x "$c" ] && export CHROME_PATH="$c" && break; done
fi
D="$1"; shift
node render/render.mjs --date "$D" "$@"
