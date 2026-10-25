#!/bin/sh
# treg CLI wrapper: maps TREG_TO from .env to TREG_TOKEN (never printed).
. "$(dirname "$0")/envload.sh"
export TREG_TOKEN="${TREG_TOKEN:-$TREG_TO}"
exec treg "$@"
