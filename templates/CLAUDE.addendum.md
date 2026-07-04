<!-- FTSO:BEGIN -->
## Fable Token-Saving Orchestrator Addendum

This block is additive. Merge it into your existing `CLAUDE.md`; do not replace
your full file with this snippet.

### Lane Routing

Fable is the orchestrator: strategy, decomposition, architecture decisions,
dispatch packets, review, synthesis, taste, and final judgment.

Route other work by shape:

- deep reasoner: hard bounded reasoning legwork
- coder: complex repo-native implementation
- fast worker: mechanical coding, docs, focused tests, and digest duty
- Codex or side worker: well-specified implementation and second opinions
- budget lane: slow non-critical batch work
- tiny lane: high-volume machine-checkable fan-out

Before delegation, score complexity, urgency, context locality, taste, and
volume. Fable owns the decision; cheaper lanes do bounded work.

### Dense Turns

Do not end a turn just because background lanes are running. A turn ends only
when the inline work queue is also empty. While lanes run, keep doing useful
orchestrator work: review, docs, issue triage, spec cleanup, verdict synthesis,
or next-step preparation.

### Cache-Preserving Waits

For short waits with no useful inline work left, use a self-extinguishing
sleep-tick instead of going dark past the 5-minute cache lifetime:

```bash
scripts/waiting_phase_on.sh
scripts/keepalive_tick.sh
```

On wake: do one small status check, process landed work densely, and re-arm
only if still waiting. When all lanes resolve, run:

```bash
scripts/waiting_phase_off.sh
```

Do not keepalive through multi-hour waits. Let the cache die once.

### Large Outputs

Fable should not read raw large diffs, logs, or reports. Ask a fast worker to
produce a bounded digest with flagged hunks, then inspect only the digest and
the flagged raw evidence.

### Run Economics

Use cheap probes for mechanism questions. Use premium ruler runs only for
release, quality, customer-facing, or final judgment claims. Record provider,
model, scenario, methodology, and proof boundary for scored runs.
<!-- FTSO:END -->
