#!/usr/bin/env bash
set -euo pipefail

STATE_DIR="${FTSO_STATE_DIR:-$HOME/.claude/state}"
LAST_TICK="${FTSO_LAST_TICK:-$STATE_DIR/fable-last-tick}"
SLEEP_SECONDS="${FTSO_KEEPALIVE_SECONDS:-250}"

mkdir -p "$(dirname "$LAST_TICK")"
touch "$LAST_TICK"
sleep "$SLEEP_SECONDS"
printf 'ftso keepalive tick %s\n' "$(date '+%H:%M:%S')"
