# Adapting Model Names

This repo is Fable-first because that is the environment these practices came
from. You can adapt the router to your own stack.

Map each lane by capability, not brand:

- premium orchestrator: best judgment, most expensive context
- deep reasoner: hard bounded analysis
- coder: high-quality repo-native implementation
- fast worker: standard mechanical work
- side worker: self-contained implementation and second opinions
- budget lane: slow non-critical batch work
- tiny lane: high-volume machine-checkable fan-out

Keep the rule: the premium orchestrator decides, delegates, reviews, and
synthesizes. Cheaper lanes do bounded work with acceptance criteria.

If your platform supports a 1-hour prompt-cache TTL, compare it against the
sleep-tick pattern for your actual wait lengths and pricing. This repo's
defaults target ordinary 5-minute cache behavior.
