#!/usr/bin/env python3
"""Knowledge-base auditor for the Saarthi framework.

Checks the knowledge-base directory for:
  - Files not indexed in knowledge-base/INDEX.md (orphans)
  - INDEX.md references that do not exist on disk (dead links)
  - Preference files missing required YAML front-matter fields
  - Preference files whose last_seen date is older than preference_decay_days
    (from framework.config.yaml) — these are stale and should be reviewed

Usage:
    python tools/audit_kb.py --root saarthi-framework
    python tools/audit_kb.py --root saarthi-framework --stale-only
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date, datetime
from pathlib import Path

from framework_checks import read_text, scan_yaml_like_keys, config_values_by_path


# ---------------------------------------------------------------------------
# Front-matter helpers
# ---------------------------------------------------------------------------

FRONT_MATTER_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)
REQUIRED_FRONT_MATTER_FIELDS = {
    "id",
    "category",
    "confidence",
    "criticality",
    "source",
    "observed_count",
    "last_seen",
}


def parse_front_matter(text: str) -> dict[str, str] | None:
    """Return key→value dict from YAML front-matter, or None if absent."""
    match = FRONT_MATTER_RE.match(text)
    if not match:
        return None
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            fields[key.strip()] = value.strip()
    return fields


# ---------------------------------------------------------------------------
# INDEX.md reference extraction
# ---------------------------------------------------------------------------

# KB subdirectories that can contain indexed entries.
KB_SUBDIRS = (
    "architecture-decisions/",
    "engineering-standards/",
    "past-learnings/",
    "preferences/",
    "reusable-patterns/",
)

# Match Markdown link paths and bare backtick paths inside tables, e.g.
#   `preferences/coding-style-typescript.md`  or  [text](preferences/foo.md)
INDEX_PATH_RE = re.compile(
    r"`(?P<bt>[^`]+\.md)`"
    r"|"
    r"\[.*?\]\((?P<link>[^)]+\.md)\)"
)


def _is_kb_path(raw: str) -> bool:
    """Return True only if the path belongs to a known KB subdirectory."""
    return any(raw.startswith(prefix) for prefix in KB_SUBDIRS)


def extract_indexed_paths(index_text: str) -> set[str]:
    """Return KB-relative file paths referenced in INDEX.md (table rows only)."""
    paths: set[str] = set()
    for match in INDEX_PATH_RE.finditer(index_text):
        raw = match.group("bt") or match.group("link")
        if raw and _is_kb_path(raw.strip()):
            paths.add(raw.strip())
    return paths


# ---------------------------------------------------------------------------
# Decay helpers
# ---------------------------------------------------------------------------

def load_decay_days(root: Path) -> int:
    """Read preference_decay_days from framework.config.yaml; default 90."""
    config_text = read_text(root / "framework.config.yaml")
    if config_text is None:
        return 90
    entries = scan_yaml_like_keys(config_text)
    values = config_values_by_path(entries)
    raw = values.get(("adaptive_learning", "preference_decay_days"), "90")
    try:
        return int(raw.strip().strip('"'))
    except ValueError:
        return 90


# ---------------------------------------------------------------------------
# Audit logic
# ---------------------------------------------------------------------------

def audit_kb(root: Path, stale_only: bool) -> int:
    """Run the full KB audit and print findings. Returns 0 (pass) or 2 (issues)."""
    kb_root = root / "knowledge-base"
    index_path = kb_root / "INDEX.md"

    if not kb_root.is_dir():
        print(f"[FAIL] knowledge-base directory not found: {kb_root}")
        return 2

    if not index_path.exists():
        print(f"[FAIL] knowledge-base/INDEX.md not found: {index_path}")
        return 2

    index_text = read_text(index_path) or ""
    indexed_paths = extract_indexed_paths(index_text)
    decay_days = load_decay_days(root)
    today = date.today()

    # Collect all markdown files in knowledge-base (skip INDEX.md at root)
    all_kb_files: list[Path] = sorted(
        p for p in kb_root.rglob("*.md")
        if p != index_path
    )

    # Map relative (to kb_root) paths for comparison
    def rel(p: Path) -> str:
        return p.relative_to(kb_root).as_posix()

    kb_rel_paths = {rel(p) for p in all_kb_files}

    # 1. Dead links (indexed but missing on disk)
    dead_links = sorted(p for p in indexed_paths if p not in kb_rel_paths)

    # 2. Orphaned files (exist on disk but not in INDEX.md)
    # We exempt README.md files at any level (they are structural, not content entries)
    orphaned = sorted(
        r for r in kb_rel_paths
        if r not in indexed_paths and not r.endswith("README.md")
    )

    # 3. Preference file checks (stale / missing front-matter)
    stale: list[str] = []
    malformed: list[str] = []
    for path in all_kb_files:
        if path.parent.name != "preferences":
            continue
        if path.name == "README.md":
            continue
        text = read_text(path) or ""
        fm = parse_front_matter(text)
        if fm is None:
            malformed.append(f"{rel(path)}: no YAML front-matter found")
            continue
        missing_fields = REQUIRED_FRONT_MATTER_FIELDS - fm.keys()
        if missing_fields:
            malformed.append(f"{rel(path)}: missing fields: {', '.join(sorted(missing_fields))}")
            continue
        last_seen_raw = fm.get("last_seen", "")
        try:
            last_seen = datetime.strptime(last_seen_raw, "%Y-%m-%d").date()
            age_days = (today - last_seen).days
            if age_days > decay_days:
                stale.append(f"{rel(path)}: last_seen={last_seen_raw} ({age_days} days ago, limit={decay_days})")
        except ValueError:
            malformed.append(f"{rel(path)}: invalid last_seen date: {last_seen_raw!r}")

    # ---------------------------------------------------------------------------
    # Output
    # ---------------------------------------------------------------------------
    issues_found = False

    if not stale_only:
        print("\n=== Knowledge-Base Audit ===")
        print(f"  KB root           : {kb_root}")
        print(f"  Indexed entries   : {len(indexed_paths)}")
        print(f"  Files on disk     : {len(kb_rel_paths)}")
        print(f"  Preference decay  : {decay_days} days")

        _section("Dead links (indexed but missing on disk)", dead_links, is_error=True)
        issues_found = issues_found or bool(dead_links)

        _section("Orphaned files (on disk but not in INDEX.md)", orphaned, is_error=False)
        issues_found = issues_found or bool(orphaned)

        _section("Malformed preference files (missing or invalid front-matter)", malformed, is_error=True)
        issues_found = issues_found or bool(malformed)

    _section(
        f"Stale preferences (last_seen > {decay_days} days ago)",
        stale,
        is_error=False,
    )
    issues_found = issues_found or bool(stale)

    if not issues_found:
        print("\n[PASS] Knowledge-base audit clean — no issues found.")
        return 0
    else:
        print("\n[WARN] Knowledge-base audit found issues — review the items above.")
        return 2


def _section(title: str, items: list[str], is_error: bool) -> None:
    mark = "[FAIL]" if is_error and items else "[WARN]" if items else "[PASS]"
    print(f"\n{mark} {title} ({len(items)} found)")
    for item in items:
        print(f"       - {item}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit the Saarthi knowledge-base for stale, orphaned, or malformed entries."
    )
    parser.add_argument(
        "--root", "-r", default=".", help="Framework root directory (default: current directory)"
    )
    parser.add_argument(
        "--stale-only",
        action="store_true",
        help="Only check for stale preferences; skip orphan/dead-link checks.",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    root = Path(args.root).resolve()
    return audit_kb(root, stale_only=args.stale_only)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
