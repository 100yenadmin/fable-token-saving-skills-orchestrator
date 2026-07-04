from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest


ROOT = Path(__file__).resolve().parents[1]
KEEPALIVE_HOOK = ROOT / "hooks" / "stop-keepalive-guard.py"
AUTONOMOUS_HOOK = ROOT / "hooks" / "stop-autonomous-guard.py"


class KeepaliveHookTests(unittest.TestCase):
    def run_hook(self, env: dict[str, str], stdin: str = "{}") -> subprocess.CompletedProcess[str]:
        merged = os.environ.copy()
        merged.update(env)
        return subprocess.run(
            [sys.executable, str(KEEPALIVE_HOOK)],
            input=stdin,
            text=True,
            capture_output=True,
            env=merged,
            check=False,
        )

    def test_allows_when_no_sentinel_exists(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = self.run_hook({
                "FTSO_KEEPALIVE_SENTINEL": str(Path(tmp) / "sentinel"),
                "FTSO_LAST_TICK": str(Path(tmp) / "tick"),
            })
            self.assertEqual(result.returncode, 0)
            self.assertEqual(result.stdout, "")

    def test_allows_when_tick_is_fresh(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            sentinel = Path(tmp) / "sentinel"
            tick = Path(tmp) / "tick"
            sentinel.touch()
            tick.touch()
            result = self.run_hook({
                "FTSO_KEEPALIVE_SENTINEL": str(sentinel),
                "FTSO_LAST_TICK": str(tick),
            })
            self.assertEqual(result.returncode, 0)
            self.assertEqual(result.stdout, "")

    def test_blocks_when_tick_is_stale(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            sentinel = Path(tmp) / "sentinel"
            tick = Path(tmp) / "tick"
            sentinel.touch()
            tick.touch()
            old = time.time() - 1000
            os.utime(tick, (old, old))
            result = self.run_hook({
                "FTSO_KEEPALIVE_SENTINEL": str(sentinel),
                "FTSO_LAST_TICK": str(tick),
                "FTSO_STALE_AFTER_SECONDS": "200",
            })
            self.assertEqual(result.returncode, 0)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["decision"], "block")
            self.assertIn("sleep-tick", payload["reason"])

    def test_invalid_json_input_fails_open_without_sentinel(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = self.run_hook({
                "FTSO_KEEPALIVE_SENTINEL": str(Path(tmp) / "sentinel"),
                "FTSO_LAST_TICK": str(Path(tmp) / "tick"),
            }, stdin="{not json")
            self.assertEqual(result.returncode, 0)
            self.assertEqual(result.stdout, "")


class AutonomousHookTests(unittest.TestCase):
    def run_hook(self, env: dict[str, str], payload: dict) -> subprocess.CompletedProcess[str]:
        merged = os.environ.copy()
        merged.update(env)
        return subprocess.run(
            [sys.executable, str(AUTONOMOUS_HOOK)],
            input=json.dumps(payload),
            text=True,
            capture_output=True,
            env=merged,
            check=False,
        )

    def write_transcript(self, path: Path, text: str) -> None:
        item = {
            "type": "assistant",
            "message": {
                "model": "claude",
                "content": [{"type": "text", "text": text}],
            },
        }
        path.write_text(json.dumps(item) + "\n", encoding="utf-8")

    def test_allows_report_when_no_active_plan_exists(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            transcript = root / "transcript.jsonl"
            self.write_transcript(transcript, "Milestone report: I will proceed next.")
            result = self.run_hook(
                {"FTSO_PLAN_GLOB": str(root / "plans" / "*.md")},
                {"transcript_path": str(transcript)},
            )
            self.assertEqual(result.returncode, 0)
            self.assertEqual(result.stdout, "")

    def test_blocks_report_only_stop_when_active_plan_exists(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            plans = root / "plans"
            plans.mkdir()
            (plans / "active.md").write_text("next: continue", encoding="utf-8")
            transcript = root / "transcript.jsonl"
            self.write_transcript(transcript, "Milestone report: I will proceed next.")
            result = self.run_hook(
                {"FTSO_PLAN_GLOB": str(plans / "*.md")},
                {"transcript_path": str(transcript)},
            )
            self.assertEqual(result.returncode, 0)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["decision"], "block")
            self.assertIn("next tool call", payload["reason"])

    def test_allows_real_blocker_question(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            plans = root / "plans"
            plans.mkdir()
            (plans / "active.md").write_text("next: continue", encoding="utf-8")
            transcript = root / "transcript.jsonl"
            self.write_transcript(transcript, "Blocked: missing credential. Can you confirm?")
            result = self.run_hook(
                {"FTSO_PLAN_GLOB": str(plans / "*.md")},
                {"transcript_path": str(transcript)},
            )
            self.assertEqual(result.returncode, 0)
            self.assertEqual(result.stdout, "")

    def test_allows_genuinely_pending_background_wake_phrase(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            plans = root / "plans"
            plans.mkdir()
            (plans / "active.md").write_text("next: continue", encoding="utf-8")
            transcript = root / "transcript.jsonl"
            self.write_transcript(
                transcript,
                "The probe is still running in the background; they'll wake this session when done.",
            )
            result = self.run_hook(
                {"FTSO_PLAN_GLOB": str(plans / "*.md")},
                {"transcript_path": str(transcript)},
            )
            self.assertEqual(result.returncode, 0)
            self.assertEqual(result.stdout, "")


if __name__ == "__main__":
    unittest.main()
