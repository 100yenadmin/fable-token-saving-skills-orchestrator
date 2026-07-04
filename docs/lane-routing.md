# Lane Routing

Fable should own judgment. It does not need to own every keystroke.

## Default Router

| Lane | Good For | Avoid |
| --- | --- | --- |
| Fable orchestrator | strategy, architecture, decomposition, dispatch packets, review, synthesis, taste, final judgment | routine typing, raw log reading, broad mechanical fan-out |
| Deep reasoner | hard root-cause work, algorithm reasoning, candidate tradeoff analysis | owning product strategy or final decisions |
| Coder | complex repo-native implementation where quality matters | trivial edits |
| Fast worker | mechanical coding, focused docs, test sweeps, large-output digesting | final judgment on hard findings |
| Codex worker | well-specified implementation, side PRs, blind second opinions, UI verification | ambiguous architecture decisions |
| GLM or other budget lane | slow non-urgent prep, batch work, off-critical-path corroboration | critical-path release evidence unless clearly labeled |
| Tiny model | huge machine-checkable fan-out with downstream verification | judging, taste, or release readiness |

## Score Before Dispatch

Before delegating, score the unit:

- complexity: trivial, standard, complex, frontier
- urgency: blocking now or parallel
- context locality: local tools needed or self-contained
- taste: user-facing judgment or mechanical
- volume: one task or many similar tasks

Use Fable for the call. Route the typing.

## Escalation

Judge the output, not the price tag. If a cheap lane misses the bar, rerun one
tier up with concrete corrective feedback. Do not keep asking the wrong lane to
guess harder.
