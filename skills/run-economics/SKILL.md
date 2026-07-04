---
name: run-economics
description: Use when choosing between cheap probes, worker runs, expensive ruler runs, or long keepalive waits.
---

# Run Economics

Match the instrument to the question.

## Mechanism

Use cheap probes when the question is "does this mechanism fire?"

Examples:

- hook blocks stale wait
- cue reaches worker
- small parser case passes
- one narrow acceptance test catches the bug

## Ruler

Use premium runs when the question is "does this meet the bar?"

Examples:

- release readiness
- final quality score
- customer-facing proof
- hard architectural judgment

## Cache

For short waits, preserve the prompt cache with a sleep-tick if no inline work
remains. For long waits, let the cache die once. Do not ping through multi-hour
idle windows by default.

## Ledger

For scored or judged runs, record provider, model or lane, scenario, method,
score, and proof boundary.
