# Dense Turns

Orchestration saves money when the orchestrator keeps doing useful work while
lanes run.

The expensive failure pattern:

1. Dispatch several lanes.
2. End the turn.
3. Wake 6 to 8 minutes later.
4. Process one notification.
5. End again.

Every gap beyond the prompt-cache lifetime can force a cold context read. The
fix is not "never dispatch." The fix is to keep the turn dense.

## Practical Rules

- End a turn only when the inline work queue is empty.
- While lanes run, do reviews, docs, issue triage, spec refinement, or verdict
  processing.
- Digest raw outputs before Fable reads them.
- Batch multiple wake results into one integration pass when possible.
- End on a watcher or keepalive only when waiting is the only useful remaining
  work.

Orchestration is for parallelism and volume. It is not a reason for the most
expensive model to sit dark.
