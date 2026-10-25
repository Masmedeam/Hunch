#!/bin/sh
# Put Hunch's exported bundle where Domino reads it: external/hunch_live/bundle.json.
# Uses this repo's own export when present (scripts/export_ui_data.py writes ui/public/data/bundle.json), else the live worker.
set -e
cd "$(dirname "$0")/.."
mkdir -p external/hunch_live
if [ -f ../../ui/public/data/bundle.json ]; then
  cp ../../ui/public/data/bundle.json external/hunch_live/bundle.json
else
  curl -sL https://nextday-prediction.hidden-pond-5e6a.workers.dev/data/bundle.json -o external/hunch_live/bundle.json
fi
echo "bundle: $(wc -c < external/hunch_live/bundle.json) bytes"
