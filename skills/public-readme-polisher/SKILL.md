---
name: public-readme-polisher
description: Use when improving a public README, repository homepage, docs landing page, or developer-facing first impression.
---

# Public README Polisher

Polish the README as the repo's public front door: credible, scannable,
actionable, and claim-safe.

## Use When

- a README feels plain
- a repo needs a public first impression
- a docs landing page needs clearer value, install path, or proof
- a visual asset could make the repo easier to understand

## Process

1. Audit repo truth: purpose, install path, tests, license, security, CI, docs,
   examples, and public claim boundaries.
2. Define the public promise in one paragraph: who it helps, what it gives
   them, and what it does not guarantee.
3. Improve the first viewport: title, optional hero, badges, concise opening,
   quick action, and a scannable "what you get" table.
4. Add scanning structure: quick start, workflow diagram when useful, proof or
   sources near the claim, and links to deeper docs.
5. Validate links, images, alt text, docs scan, tests, and the scorecard below.

## Visual Asset Rules

- Use one purposeful hero only when it clarifies the repo.
- For generated images: no embedded text, no logos, no watermarks.
- Inspect the image before committing; reject generated image with readable fake
  text, broken UI, mascot drift, or misleading claims.
- Save README assets under `assets/readme`.
- Add alt text that explains the image function.

## Claim Safety

- Cite official sources for factual pricing, cache, legal, API, or security
  claims.
- Say "patterns that worked for us" for experience-based recommendations.
- Avoid guaranteed savings, official endorsement, universal safety claims, or
  "works for every workflow" language.
- Keep related tools optional unless the repo truly depends on them.

## Scorecard

Score each category 0-2. Pass at 13/16 or higher.

| Category | 2 means |
| --- | --- |
| First-viewport signal | repo purpose, visual tone, badges, and install path are clear without scrolling |
| Audience/value clarity | reader knows who it is for and what problem it solves |
| Scannability | tables, bullets, headings, and diagrams make scanning easy |
| Actionability | quick start and next links are concrete and current |
| Trust/proof | sources, CI, license, tests, and safety boundaries support the claims |
| Visual polish | assets feel intentional, domain-fit, and not generic stock decoration |
| Accessibility/asset hygiene | alt text, local paths, file size, and image rendering are sane |
| Claim safety | claims are bounded, sourced where needed, and public-safe |

Automatic blockers: private paths, secrets, broken local links, missing install
path, false or guaranteed claims, generated image with readable fake text,
missing alt text, failing docs scan.

## Common Mistakes

- Making a marketing page that hides the actual install/use path.
- Adding a pretty image that does not explain the repo.
- Moving official citations away from the claims they support.
- Replacing precise safety boundaries with vague hype.
- Claiming completion without running the scorecard.
