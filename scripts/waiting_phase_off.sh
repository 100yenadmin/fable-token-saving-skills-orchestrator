#!/usr/bin/env bash
set -euo pipefail

STATE_DIR="${FTSO_STATE_DIR:-$HOME/.claude/state}"
SENTINEL="${FTSO_KEEPALIVE_SENTINEL:-$STATE_DIR/fable-keepalive-required}"

rm -f "$SENTINEL"
printf 'ftso waiting phase off: %s\n' "$SENTINEL"
