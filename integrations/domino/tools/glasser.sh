#!/bin/sh
# Glasser CLI wrapper: Node 22 from nvm, plus the OS trust store (this network's TLS chain is not in Node's bundled CAs).
# Maps GLASSER from .env to GLASSER_API_KEY (never printed).
. "$(dirname "$0")/envload.sh"
export GLASSER_API_KEY="${GLASSER_API_KEY:-$GLASSER}"
export PATH="$HOME/.nvm/versions/node/v22.22.2/bin:$PATH"
export NODE_OPTIONS="--use-system-ca ${NODE_OPTIONS:-}"
exec glasser "$@"
