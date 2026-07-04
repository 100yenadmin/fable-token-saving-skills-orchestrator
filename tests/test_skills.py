from __future__ import annotations

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "public-readme-polisher" / "SKILL.md"


class PublicReadmePolisherSkillTests(unittest.TestCase):
    def test_skill_frontmatter_uses_trigger_style_description(self) -> None:
        text = SKILL.read_text(encoding="utf-8")
        match = re.match(r"---\nname: public-readme-polisher\ndescription: (.+?)\n---", text)
        self.assertIsNotNone(match)
        description = match.group(1)
        self.assertTrue(description.startswith("Use when "))
        self.assertNotIn("scorecard", description.lower())
        self.assertNotIn("workflow", description.lower())

    def test_skill_contains_scorecard_and_blockers(self) -> None:
        text = SKILL.read_text(encoding="utf-8").lower()
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
        text = SKILL.read_text(encoding="utf-8").lower()
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


if __name__ == "__main__":
    unittest.main()
