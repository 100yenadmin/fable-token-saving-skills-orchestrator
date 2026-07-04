#!/usr/bin/env python3
"""Fail-open Stop hook for short-wait keepalive discipline.

When a waiting sentinel exists, the agent should end the turn by arming a
sleep-tick task before the prompt cache expires. If the sentinel exists and no
tick marker was touched recently, this hook blocks the stop with a concrete
repair instruction.

Environment overrides:
  FTSO_KEEPALIVE_SENTINEL
  FTSO_LAST_TICK
  FTSO_STALE_AFTER_SECONDS
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import sys
import time


def default_state_path(name: str) -> str:
    return str(Path.home() / ".claude" / "state" / name)


SENTINEL = os.environ.get(
    "FTSO_KEEPALIVE_SENTINEL",
    default_state_path("fable-keepalive-required"),
)
LAST_TICK = os.environ.get(
    "FTSO_LAST_TICK",
    default_state_path("fable-last-tick"),
)
STALE_AFTER_SECONDS = int(os.environ.get("FTSO_STALE_AFTER_SECONDS", "200"))


def allow() -> int:
    return 0


def main() -> int:
    try:
        try:
            json.load(sys.stdin)
        except Exception:
            pass

        sentinel = Path(SENTINEL)
        if not sentinel.exists():
            return allow()

        tick = Path(LAST_TICK)
        age = time.time() - tick.stat().st_mtime if tick.exists() else 1_000_000_000
        if age <= STALE_AFTER_SECONDS:
            return allow()

        reason = (
            "FTSO keepalive guard: a waiting sentinel exists, but no recent "
            "sleep-tick was armed. Arm one as the final action, for example: "
            "`scripts/keepalive_tick.sh`. If all lanes are resolved or the wait "
            "is deliberately long, clear the sentinel with "
            "`scripts/waiting_phase_off.sh` instead."
        )
        print(json.dumps({"decision": "block", "reason": reason}))
        return allow()
    except Exception:
        return allow()


if __name__ == "__main__":
    raise SystemExit(main())
