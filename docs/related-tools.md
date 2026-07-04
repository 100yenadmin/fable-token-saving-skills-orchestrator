# Related Tools And Inspirations

FTSO is standalone: you can use the addendum, hooks, skills, and docs in this
repo without installing any project listed here. These links are included so
readers can find adjacent tooling and understand the prior-art boundary.

## openai/codex-plugin-cc

Link: [openai/codex-plugin-cc](https://github.com/openai/codex-plugin-cc)

Use it when a Claude Code user wants slash-command access to Codex review,
adversarial review, rescue, transfer, status, result, or cancel workflows from
inside Claude Code.

FTSO boundary: optional adjacent tool. It can be a convenient way to reach Codex
from Claude Code, but FTSO does not require it. Background jobs, review gates,
and delegated runs should still follow dense-turn and wait-discipline rules so
usage does not drift upward.

License noted upstream: Apache-2.0.

## blader/arbitrage

Link: [blader/arbitrage](https://github.com/blader/arbitrage)

Use it when you want a compact Claude Code skill centered on the premium-model
judgment plus Codex implementation pattern.

FTSO boundary: inspiration and prior art for the token-arbitrage framing. FTSO
generalizes that idea into a broader Fable-first kit: additive Claude
configuration, cache-preserving wait discipline, Stop hooks, installer safety,
lane routing, run economics, and public-safe templates.

License noted upstream: MIT.
