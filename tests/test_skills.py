from __future__ import annotations

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
README_POLISHER = ROOT / "skills" / "public-readme-polisher" / "SKILL.md"
REPO_OPERATIONALIZER = ROOT / "skills" / "public-repo-operationalizer" / "SKILL.md"


class PublicReadmePolisherSkillTests(unittest.TestCase):
    def test_skill_frontmatter_uses_trigger_style_description(self) -> None:
        text = README_POLISHER.read_text(encoding="utf-8")
        match = re.match(r"---\nname: public-readme-polisher\ndescription: (.+?)\n---", text)
        self.assertIsNotNone(match)
        description = match.group(1)
        self.assertTrue(description.startswith("Use when "))
        self.assertNotIn("scorecard", description.lower())
        self.assertNotIn("workflow", description.lower())

    def test_skill_contains_scorecard_and_blockers(self) -> None:
        text = README_POLISHER.read_text(encoding="utf-8").lower()
        required_terms = [
            "scorecard",
            "first-viewport signal",
            "audience/value clarity",
            "scannability",
            "actionability",
            "trust/proof",
            "visual polish",
            "accessibility/asset hygiene",
            "claim safety",
            "13/16",
            "automatic blockers",
            "private paths",
            "secrets",
            "broken local links",
            "generated image with readable fake text",
            "missing alt text",
            "failing docs scan",
        ]
        for term in required_terms:
            with self.subTest(term=term):
                self.assertIn(term, text)

    def test_skill_contains_asset_and_claim_safety_rules(self) -> None:
        text = README_POLISHER.read_text(encoding="utf-8").lower()
        required_terms = [
            "assets/readme",
            "inspect the image",
            "no embedded text",
            "no logos",
            "no watermarks",
            "alt text",
            "patterns that worked for us",
            "guaranteed savings",
            "official endorsement",
            "cite official sources",
        ]
        for term in required_terms:
            with self.subTest(term=term):
                self.assertIn(term, text)


class PublicRepoOperationalizerSkillTests(unittest.TestCase):
    def test_skill_frontmatter_uses_trigger_style_description(self) -> None:
        text = REPO_OPERATIONALIZER.read_text(encoding="utf-8")
        match = re.match(r"---\nname: public-repo-operationalizer\ndescription: (.+?)\n---", text)
        self.assertIsNotNone(match)
        description = match.group(1)
        self.assertTrue(description.startswith("Use when "))
        self.assertNotIn("scorecard", description.lower())
        self.assertNotIn("workflow", description.lower())

    def test_skill_contains_operational_readiness_contract(self) -> None:
        text = REPO_OPERATIONALIZER.read_text(encoding="utf-8").lower()
        required_terms = [
            "public repo operational status",
            "readme",
            "contributing.md",
            "security.md",
            "license",
            "issue templates",
            "pull request template",
            "claim audit",
            "source authority",
            "proof boundary",
            "setup path",
            "ci",
            "docs safety scan",
            "redaction",
            "no raw transcripts",
            "no private paths",
        ]
        for term in required_terms:
            with self.subTest(term=term):
                self.assertIn(term, text)

    def test_skill_contains_scorecard_and_blockers(self) -> None:
        text = REPO_OPERATIONALIZER.read_text(encoding="utf-8").lower()
        required_terms = [
            "score each category 0-2",
            "pass at 14/18",
            "first-run path",
            "template completeness",
            "claim safety",
            "source/proof authority",
            "contributor safety",
            "validation automation",
            "release readiness",
            "automatic blockers",
            "secret",
            "broken required setup command",
            "unbounded claim",
            "missing license",
        ]
        for term in required_terms:
            with self.subTest(term=term):
                self.assertIn(term, text)

    def test_readme_mentions_operationalizer_skill(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8").lower()
        self.assertIn("public repo operational", readme)
        self.assertIn("readme polish", readme)


if __name__ == "__main__":
    unittest.main()
