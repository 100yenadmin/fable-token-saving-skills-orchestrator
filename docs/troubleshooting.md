# Troubleshooting

## The Stop Hook Blocks Too Often

Check whether the waiting sentinel still exists:

```bash
ls "$HOME/.claude/state/fable-keepalive-required"
```

If no lanes are pending, clear it:

```bash
scripts/waiting_phase_off.sh
```

## The Hook Never Blocks

Confirm it is registered in `settings.json` and copied to `~/.claude/hooks`.
Run the installer in dry-run mode to see what it expects:

```bash
python3 scripts/install.py --dry-run
```

## I Do Not Use GLM

No problem. Treat GLM as an example budget lane. Replace it with your own
provider or remove the lane from the addendum.

## My Tasks Take More Than An Hour

Let the cache die once, or use your platform's longer cache TTL if it is
available and cheaper for your workload. Do not ping through multi-hour idle
windows by default.

## I Already Have A Large CLAUDE.md

That is the expected case. Use the marked addendum block and keep your current
instructions. This repo is additive, not replacement guidance.
