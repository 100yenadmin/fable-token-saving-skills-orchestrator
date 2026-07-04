# Contributing

Thanks for helping make high-end agent orchestration less wasteful.

## Development Loop

1. Open or reuse a GitHub issue.
2. Keep changes focused and public-safe.
3. Run the focused checks:

   ```bash
   python3 -m unittest discover -s tests
   python3 scripts/check_docs.py
   ```

4. Open a pull request that links the issue.

## Public-Safety Rules

- Do not commit credentials, raw transcripts, customer data, cookies, private
  connector URLs, or machine-local paths.
- Keep `CLAUDE.md` guidance additive. Users should copy a marked section into
  their existing file, not replace the whole file.
- Hooks must be idempotent and fail-open.
- Installer changes must default to dry-run and require `--apply` for mutation.
- Cost-saving claims must be framed as practice notes, not guarantees.

## Documentation Style

Write for people who are excellent builders but new to Fable orchestration.
Prefer concrete examples, short command snippets, and explicit proof
boundaries over grand claims.
