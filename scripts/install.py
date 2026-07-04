#!/usr/bin/env python3
"""Install FTSO hooks, skills, and additive CLAUDE.md guidance."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import sys
import time
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
ADDENDUM = ROOT / "templates" / "CLAUDE.addendum.md"
HOOKS = [
    ROOT / "hooks" / "stop-keepalive-guard.py",
    ROOT / "hooks" / "stop-autonomous-guard.py",
]
SKILL_DIRS = [
    ROOT / "skills" / "fable-orchestrator-router",
    ROOT / "skills" / "codex-dispatch",
    ROOT / "skills" / "run-economics",
    ROOT / "skills" / "public-readme-polisher",
    ROOT / "skills" / "public-repo-operationalizer",
]
BEGIN_MARKER = "<!-- FTSO:BEGIN -->"
END_MARKER = "<!-- FTSO:END -->"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="print actions only; default")
    mode.add_argument("--apply", action="store_true", help="apply changes")
    parser.add_argument("--claude-home", default=str(Path.home() / ".claude"))
    parser.add_argument("--install-hooks", action="store_true")
    parser.add_argument("--install-skills", action="store_true")
    parser.add_argument("--append-addendum", action="store_true")
    return parser.parse_args()


def selected_actions(args: argparse.Namespace) -> set[str]:
    chosen = set()
    if args.install_hooks:
        chosen.add("hooks")
    if args.install_skills:
        chosen.add("skills")
    if args.append_addendum:
        chosen.add("addendum")
    return chosen or {"hooks", "skills", "addendum"}


def log(message: str) -> None:
    print(message)


def backup(path: Path) -> Path | None:
    if not path.exists():
        return None
    stamp = time.strftime("%Y%m%d-%H%M%S")
    backup_path = path.with_name(f"{path.name}.bak-ftso-{stamp}")
    shutil.copy2(path, backup_path)
    return backup_path


def copy_file(src: Path, dst: Path, apply: bool) -> None:
    log(f"{'copy' if apply else 'would copy'} {src.relative_to(ROOT)} -> {dst}")
    if apply:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        if dst.suffix in {".py", ".sh"}:
            dst.chmod(0o755)


def copy_tree(src: Path, dst: Path, apply: bool) -> None:
    log(f"{'sync' if apply else 'would sync'} {src.relative_to(ROOT)} -> {dst}")
    if not apply:
        return
    if dst.exists():
        shutil.rmtree(dst)
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(src, dst)


def hook_entry(script: Path) -> dict:
    command = f'python3 "{script}"'
    name = script.name.replace(".py", "")
    return {
        "matcher": "*",
        "hooks": [
            {
                "type": "command",
                "command": command,
                "timeout": 5,
                "statusMessage": f"FTSO {name}: checking stop discipline...",
            }
        ],
    }


def existing_stop_hook_script_names(stop_hooks: list[dict]) -> set[str]:
    script_names = {hook.name for hook in HOOKS}
    existing: set[str] = set()
    for entry in stop_hooks:
        for hook in entry.get("hooks", []):
            if not isinstance(hook, dict):
                continue
            command = hook.get("command", "")
            for name in script_names:
                if name in command:
                    existing.add(name)
    return existing


def register_hooks(settings_path: Path, hook_paths: Iterable[Path], apply: bool) -> None:
    log(f"{'update' if apply else 'would update'} {settings_path} Stop hooks")
    if not apply:
        return
    settings_path.parent.mkdir(parents=True, exist_ok=True)
    data = {}
    if settings_path.exists():
        backup_path = backup(settings_path)
        if backup_path:
            log(f"backup {settings_path} -> {backup_path}")
        data = json.loads(settings_path.read_text(encoding="utf-8") or "{}")
    hooks = data.setdefault("hooks", {})
    stop_hooks = hooks.setdefault("Stop", [])
    existing_scripts = existing_stop_hook_script_names(stop_hooks)
    for path in hook_paths:
        entry = hook_entry(path)
        if path.name in existing_scripts:
            continue
        stop_hooks.append(entry)
        existing_scripts.add(path.name)
    settings_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def append_addendum(claude_md: Path, apply: bool) -> None:
    text = ADDENDUM.read_text(encoding="utf-8").strip() + "\n"
    log(f"{'append' if apply else 'would append'} marked addendum -> {claude_md}")
    if not apply:
        return
    claude_md.parent.mkdir(parents=True, exist_ok=True)
    current = claude_md.read_text(encoding="utf-8") if claude_md.exists() else ""
    if BEGIN_MARKER in current and END_MARKER in current:
        log("addendum already present; skipping")
        return
    backup_path = backup(claude_md)
    if backup_path:
        log(f"backup {claude_md} -> {backup_path}")
    separator = "\n\n" if current and not current.endswith("\n\n") else ""
    claude_md.write_text(current + separator + text, encoding="utf-8")


def main() -> int:
    args = parse_args()
    apply = bool(args.apply)
    if not apply:
        log("dry-run mode; pass --apply to write changes")
    claude_home = Path(args.claude_home).expanduser().resolve()
    actions = selected_actions(args)

    installed_hook_paths = [claude_home / "hooks" / hook.name for hook in HOOKS]
    if "hooks" in actions:
        for src, dst in zip(HOOKS, installed_hook_paths):
            copy_file(src, dst, apply)
        register_hooks(claude_home / "settings.json", installed_hook_paths, apply)

    if "skills" in actions:
        for src in SKILL_DIRS:
            copy_tree(src, claude_home / "skills" / src.name, apply)

    if "addendum" in actions:
        append_addendum(claude_home / "CLAUDE.md", apply)

    log("complete" if apply else "dry-run complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
