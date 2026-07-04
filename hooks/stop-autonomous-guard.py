#!/usr/bin/env python3
"""Fail-open Stop hook for report-only autonomous stops.

This catches the common long-run failure where an agent writes a milestone
summary or "I will proceed next" paragraph while plan work remains, then stops
without emitting the next tool call.
"""
from __future__ import annotations

import glob
import json
import os
import re
import sys
import time


REPORT_PATTERN = re.compile(
    r"i'?ll proceed|i will proceed|milestone (report|summary|complete)|"
    r"clean checkpoint|wrapping up|next session|the plan is complete|"
    r"no open prs",
    re.IGNORECASE,
)
BLOCKER_PATTERN = re.compile(
    r"\?\s*$|blocked|waiting on you|need your|permission|confirm|"
    r"missing credential|safety gate|do you want|should i\b",
    re.IGNORECASE,
)
PENDING_PATTERN = re.compile(
    r"background .*?(running|pending|in flight)|auto-?wake|watcher .*?(active|running)|"
    r"will resume when|when .*?(done|complete|finished)",
    re.IGNORECASE,
)


def allow() -> int:
    return 0


def active_plan_exists() -> bool:
    plan_glob = os.environ.get(
        "FTSO_PLAN_GLOB",
        str(os.path.expanduser("~/.claude/plans/*.md")),
    )
    horizon = int(os.environ.get("FTSO_ACTIVE_PLAN_SECONDS", "21600"))
    now = time.time()
    return any(
        os.path.isfile(path) and now - os.path.getmtime(path) < horizon
        for path in glob.glob(plan_glob)
    )


def last_assistant_text(transcript_path: str) -> str:
    text = ""
    with open(transcript_path, encoding="utf-8") as handle:
        for line in handle:
            if '"assistant"' not in line:
                continue
            try:
                item = json.loads(line)
            except Exception:
                continue
            if item.get("type") != "assistant":
                continue
            message = item.get("message", {}) or {}
            if message.get("model") == "<synthetic>":
                continue
            content = message.get("content", "")
            if isinstance(content, list):
                candidate = "".join(
                    block.get("text", "")
                    for block in content
                    if isinstance(block, dict) and block.get("type") == "text"
                )
            else:
                candidate = str(content)
            if candidate.strip():
                text = candidate
    return text


def main() -> int:
    try:
        try:
            data = json.load(sys.stdin)
        except Exception:
            return allow()

        if data.get("stop_hook_active"):
            return allow()
        if not active_plan_exists():
            return allow()

        transcript_path = data.get("transcript_path", "")
        if not transcript_path or not os.path.isfile(transcript_path):
            return allow()

        text = last_assistant_text(transcript_path)
        if not text.strip():
            return allow()

        if (
            REPORT_PATTERN.search(text)
            and not BLOCKER_PATTERN.search(text)
            and not PENDING_PATTERN.search(text)
        ):
            reason = (
                "FTSO autonomous guard: this stop looks like a milestone report "
                "or stated-next turn while an active plan exists. Do the next "
                "tool call instead. If there is a real blocker, state the one "
                "specific question. If background work will auto-wake this "
                "thread, say that explicitly."
            )
            print(json.dumps({"decision": "block", "reason": reason}))
        return allow()
    except Exception:
        return allow()


if __name__ == "__main__":
    raise SystemExit(main())
