# Agent Instructions

This repository packages public Fable orchestration practices.

## Before Editing

1. Read `README.md` for the public promise and proof boundary.
2. Read `SECURITY.md` before touching hooks, installer behavior, credentials,
   or private-data handling.
3. Create or reuse a GitHub issue before meaningful implementation work.
4. Keep all examples public-safe.

## Invariants

- `CLAUDE.md` content is additive, not replacement guidance.
- Installer behavior defaults to dry-run and requires `--apply` for mutation.
- Hooks must be idempotent and fail-open.
- Never add hardcoded API tokens, cookies, raw transcripts, customer data, or
  machine-local private paths.
- Keep Fable-first language, but make lane names configurable.
- Do not claim guaranteed savings or official endorsement.

## Validation

Run focused checks before PR readiness claims:

```bash
python3 -m unittest discover -s tests
python3 scripts/check_docs.py
```
