from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
INSTALL = ROOT / "scripts" / "install.py"


class InstallTests(unittest.TestCase):
    def run_install(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(INSTALL), *args],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_dry_run_does_not_create_claude_home(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "claude-home"
            result = self.run_install("--dry-run", "--claude-home", str(target))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("dry-run mode", result.stdout)
            self.assertFalse(target.exists())

    def test_apply_installs_all_surfaces_and_backups_settings(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "claude-home"
            home.mkdir()
            (home / "settings.json").write_text(json.dumps({"hooks": {"Stop": []}}), encoding="utf-8")
            result = self.run_install("--apply", "--claude-home", str(home))
            self.assertEqual(result.returncode, 0, result.stderr)

            self.assertTrue((home / "hooks" / "stop-keepalive-guard.py").exists())
            self.assertTrue((home / "hooks" / "stop-autonomous-guard.py").exists())
            self.assertTrue((home / "skills" / "fable-orchestrator-router" / "SKILL.md").exists())
            self.assertTrue((home / "skills" / "public-readme-polisher" / "SKILL.md").exists())
            self.assertTrue((home / "CLAUDE.md").exists())
            self.assertIn("FTSO:BEGIN", (home / "CLAUDE.md").read_text(encoding="utf-8"))
            backups = list(home.glob("settings.json.bak-ftso-*"))
            self.assertEqual(len(backups), 1)

            settings = json.loads((home / "settings.json").read_text(encoding="utf-8"))
            stop_hooks = settings["hooks"]["Stop"]
            commands = json.dumps(stop_hooks)
            self.assertIn("stop-keepalive-guard.py", commands)
            self.assertIn("stop-autonomous-guard.py", commands)

    def test_apply_is_idempotent_for_addendum_and_hook_registration(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "claude-home"
            first = self.run_install("--apply", "--claude-home", str(home))
            second = self.run_install("--apply", "--claude-home", str(home))
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual(second.returncode, 0, second.stderr)

            claude_text = (home / "CLAUDE.md").read_text(encoding="utf-8")
            self.assertEqual(claude_text.count("FTSO:BEGIN"), 1)
            settings = json.loads((home / "settings.json").read_text(encoding="utf-8"))
            commands = [
                hook["hooks"][0]["command"]
                for hook in settings["hooks"]["Stop"]
                if hook.get("hooks")
            ]
            self.assertEqual(len(commands), len(set(commands)))

    def test_existing_template_hook_entries_are_not_duplicated(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "claude-home"
            home.mkdir()
            (home / "settings.json").write_text(json.dumps({
                "hooks": {
                    "Stop": [
                        {
                            "matcher": "*",
                            "hooks": [
                                {
                                    "type": "command",
                                    "command": 'python3 "$HOME/.claude/hooks/stop-keepalive-guard.py"',
                                    "timeout": 5,
                                }
                            ],
                        }
                    ]
                }
            }), encoding="utf-8")
            result = self.run_install("--apply", "--claude-home", str(home), "--install-hooks")
            self.assertEqual(result.returncode, 0, result.stderr)
            settings = json.loads((home / "settings.json").read_text(encoding="utf-8"))
            commands = [
                hook["hooks"][0]["command"]
                for hook in settings["hooks"]["Stop"]
                if hook.get("hooks")
            ]
            keepalive_count = sum("stop-keepalive-guard.py" in command for command in commands)
            autonomous_count = sum("stop-autonomous-guard.py" in command for command in commands)
            self.assertEqual(keepalive_count, 1)
            self.assertEqual(autonomous_count, 1)

    def test_partial_hook_install_does_not_append_addendum(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "claude-home"
            result = self.run_install("--apply", "--claude-home", str(home), "--install-hooks")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((home / "hooks" / "stop-keepalive-guard.py").exists())
            self.assertFalse((home / "CLAUDE.md").exists())
            self.assertFalse((home / "skills").exists())

    def test_partial_skill_install_copies_public_readme_polisher(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "claude-home"
            result = self.run_install("--apply", "--claude-home", str(home), "--install-skills")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((home / "skills" / "public-readme-polisher" / "SKILL.md").exists())
            self.assertFalse((home / "hooks").exists())
            self.assertFalse((home / "CLAUDE.md").exists())


if __name__ == "__main__":
    unittest.main()
