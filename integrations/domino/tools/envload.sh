# Sourced by tools/*.sh: export KEY=VALUE pairs from ../.env without printing them.
# Tolerates `KEY = "value"` (spaces around '=', quotes) and `export KEY=...`; skips comments and malformed lines.
_envfile="$(dirname "$0")/../.env"
if [ -f "$_envfile" ]; then
  while IFS= read -r _line || [ -n "$_line" ]; do
    case "$_line" in ''|'#'*) continue ;; esac
    _line="${_line#export }"
    _k="${_line%%=*}"
    [ "$_k" = "$_line" ] && continue
    _v="${_line#*=}"
    _k="$(printf '%s' "$_k" | tr -d '[:space:]')"
    _v="$(printf '%s' "$_v" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//' -e 's/^"\(.*\)"$/\1/' -e "s/^'\(.*\)'$/\1/")"
    case "$_k" in ''|*[!A-Za-z0-9_]*) continue ;; esac
    export "$_k=$_v"
  done < "$_envfile"
fi
unset _envfile _line _k _v
