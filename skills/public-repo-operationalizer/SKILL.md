---
name: public-repo-operationalizer
description: Use when preparing a repository, project kit, plugin, skillpack, or developer tool for public release or maintainer-ready public operations.
---

# Public Repo Operationalizer

Turn a useful repo into a public repo operational status surface: understandable,
safe to contribute to, clear about proof, and maintainable without private
context.

## Core Pattern

1. Audit repo truth: purpose, license, setup path, tests, CI, release state,
   security posture, private-data boundaries, and current claims.
2. Define the public promise: what works, what is advisory, what is unproven,
   and what the repo does not claim.
3. Add or repair default surfaces: `README.md`, `LICENSE`, `SECURITY.md`,
   `CONTRIBUTING.md`, `AGENTS.md`, `.github/ISSUE_TEMPLATE/*`,
   `.github/PULL_REQUEST_TEMPLATE.md`, and focused CI.
4. Add claim/proof docs when claims could drift: claim audit, source authority,
   proof boundary, release status, and setup path.
5. Wire validation: docs safety scan, tests, link/image checks,
   installer/package checks, and CI.
6. Close with evidence: issue/PR, commands, CI URL, risks, and next action.

## Public Safety Rules

- Do not publish raw transcripts, credentials, tokens, private paths, customer
  data, local stores, browser/session data, or screenshots with secrets.
- Say "patterns that worked for us" for practice-based guidance.
- Cite official sources near factual pricing, cache, API, legal, or security
  claims.
- Keep optional tools optional unless the repo truly depends on them.

## Default Template Bar

Contributor-facing templates should force safe evidence:

- issue templates: public-safe reproduction and redacted logs
- docs bug templates: wrong public claim or setup step
- pull request template: linked issue, changed files, validation, safety
  boundary, claim impact, rollback notes, and agent-authored disclosure

## Scorecard

Score each category 0-2. Pass at 14/18 or higher.

| Category | 2 means |
| --- | --- |
| Public promise | README says who it helps, what it does, and what it does not prove |
| First-run path | clone/install/setup/run commands work from a fresh checkout |
| Template completeness | README, license, security, contributing, AGENTS, issue templates, and pull request template fit the repo |
| Claim safety | allowed and forbidden claims are explicit and sourced where needed |
| Source/proof authority | authoritative vs advisory sources and proof boundary are clear |
| Contributor safety | redaction, no raw transcripts, no secrets, and no private paths are enforced |
| Validation automation | CI, docs safety scan, tests, and link/image checks cover the public surface |
| Release readiness | release tags, package channels, notes, or "not released yet" are clear |
| Maintainer handoff | issue/PR/evidence paths let a future agent resume |

Automatic blockers: secret, private path, raw transcript, missing license,
broken required setup command, missing install path, unbounded claim, official
endorsement claim, universal safety/savings claim, broken required local link,
or failing docs safety scan.

## Common Mistakes

- Treating README polish as operational readiness.
- Copying mature-repo machinery into a small v1 kit.
- Saying "ready" without setup-path and CI evidence.
