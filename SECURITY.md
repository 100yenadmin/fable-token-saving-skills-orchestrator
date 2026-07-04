# Security Policy

## Reporting A Vulnerability

Please open a private GitHub security advisory or contact the maintainer
privately before publishing details.

High-priority issues include:

- installer behavior that overwrites a user's existing `CLAUDE.md`
- hooks that can block stops indefinitely or fail closed
- hardcoded API tokens, cookies, connector URLs, or private keys
- public examples containing raw transcripts or private local paths
- settings mutations without a backup and an explicit `--apply`

## Local Privacy Boundary

This project is a local configuration kit. Do not attach private Claude/Codex
transcripts, auth files, cookies, tokens, screenshots with secrets, or local
machine paths to public issues.
