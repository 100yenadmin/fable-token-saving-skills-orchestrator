# Install Guide

The kit is designed to be additive. It should extend your existing Claude
configuration, not replace it.

## Dry Run

```bash
python3 scripts/install.py --dry-run --claude-home "$HOME/.claude"
```

Dry-run prints the actions that would be taken and does not create or edit
files.

## Apply

```bash
python3 scripts/install.py --apply --claude-home "$HOME/.claude"
```

When no specific install flags are provided, `--apply` installs hooks, skills,
and the `CLAUDE.md` addendum. You can also install one surface at a time:

```bash
python3 scripts/install.py --apply --install-hooks
python3 scripts/install.py --apply --install-skills
python3 scripts/install.py --apply --append-addendum
```

## What Changes

- Hooks are copied to `~/.claude/hooks`.
- Skills are copied to `~/.claude/skills`.
- Stop hooks are registered in `~/.claude/settings.json`.
- A marked FTSO block is appended to `~/.claude/CLAUDE.md`.
- Existing `settings.json` and `CLAUDE.md` files are backed up first.

The installer is idempotent. Running it again should not duplicate hook entries
or duplicate the marked `CLAUDE.md` block.

## Uninstall

Manual uninstall is intentionally simple:

1. Remove the `FTSO:BEGIN` to `FTSO:END` block from `CLAUDE.md`.
2. Remove the two FTSO Stop hook entries from `settings.json`.
3. Delete copied hooks or skills you no longer want.
