---
name: codex-dispatch
description: Use when routing well-specified implementation work from Fable to Codex or another side worker.
---

# Codex Dispatch

Premium tokens buy judgment. Codex or side-worker capacity buys implementation
volume when the task is well specified.

## Dispatch When

- the task is self-contained
- the spec carries enough context
- acceptance criteria are explicit
- the work can happen on a side branch or bounded file set
- Fable can review the result instead of typing it

## Keep With Fable Or A Higher Local Lane When

- the task is architecture, product strategy, or final judgment
- the implementation depends on local-only tools the side worker lacks
- the acceptance criteria are unclear
- the task requires private credentials or live user action

## Dispatch Packet

Include:

- objective
- repo/path/branch
- files or areas involved
- constraints and non-goals
- pseudocode for hard parts
- exact validation command or CI gate
- proof boundary
- expected final report shape

## Review Rule

If the diff or report is large, ask a fast worker for a bounded digest first.
Fable reads the digest and flagged hunks, not the whole raw output.
