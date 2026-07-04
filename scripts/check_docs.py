#!/usr/bin/env python3
"""Public-safety scan for docs, templates, scripts, hooks, skills, and tests."""
from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCAN_SUFFIXES = {".md", ".py", ".sh", ".json", ".yml", ".yaml", ".txt"}
SKIP_PARTS = {".git", "__pycache__", ".pytest_cache"}


FORBIDDEN_LITERAL_PARTS = [
    ("/Users", "/lume"),
    ("/tmp", "/worldos"),
]
PRIVATE_PATH_REGEXES = [
    re.compile(r"/Users/[A-Za-z0-9._-]+(?:/|$)"),
    re.compile(r"/home/[A-Za-z0-9._-]+(?:/|$)"),
    re.compile("/Vol" + r"umes/[A-Za-z0-9._-]+(?:/|$)"),
]
FORBIDDEN_REGEXES = [
    re.compile(r"npm_[A-Za-z0-9_]{20,}"),
    re.compile(r"ANTHROPIC_AUTH_TOKEN\s*=\s*['\"]?[A-Za-z0-9._-]{16,}"),
    re.compile(r"api[_-]?key\s*[:=]\s*['\"][A-Za-z0-9._-]{20,}", re.IGNORECASE),
    re.compile("7570c7b2" + "ebcc42b5815f401780ddd252", re.IGNORECASE),
]
MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def iter_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if any(part in SKIP_PARTS for part in path.parts):
            continue
        if path.is_file() and path.suffix in SCAN_SUFFIXES:
            files.append(path)
    return files


def check_forbidden(files: list[Path]) -> list[str]:
    errors: list[str] = []
    for path in files:
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(ROOT)
        for left, right in FORBIDDEN_LITERAL_PARTS:
            forbidden = left + right
            if forbidden in text:
                errors.append(f"{rel}: contains forbidden literal {forbidden}")
        for regex in PRIVATE_PATH_REGEXES:
            if regex.search(text):
                errors.append(f"{rel}: contains private local path matching {regex.pattern}")
        for regex in FORBIDDEN_REGEXES:
            if regex.search(text):
                errors.append(f"{rel}: matches forbidden secret pattern {regex.pattern}")
    return errors


def check_links(files: list[Path]) -> list[str]:
    errors: list[str] = []
    for path in files:
        if path.suffix != ".md":
            continue
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(ROOT)
        for match in MARKDOWN_LINK.finditer(text):
            target = match.group(1).split("#", 1)[0]
            if not target or re.match(r"^[a-z]+:", target) or target.startswith("mailto:"):
                continue
            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(ROOT)
            except ValueError:
                errors.append(f"{rel}: link escapes repo: {target}")
                continue
            if not resolved.exists():
                errors.append(f"{rel}: broken link: {target}")
    return errors


def check_readme_additive() -> list[str]:
    readme = (ROOT / "README.md").read_text(encoding="utf-8").lower()
    required = ["additive", "not a replacement"]
    missing = [term for term in required if term not in readme]
    return [f"README.md: missing required phrase {term!r}" for term in missing]


def main() -> int:
    files = iter_files()
    errors = check_forbidden(files) + check_links(files) + check_readme_additive()
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print(f"public docs safety scan passed ({len(files)} files)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
