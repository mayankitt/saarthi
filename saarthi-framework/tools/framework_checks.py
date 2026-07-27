#!/usr/bin/env python3

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class ConfigEntry:
    path: tuple[str, ...]
    value: str
    line_no: int
    indent: int


def read_text(file_path: Path) -> str | None:
    try:
        return file_path.read_text(encoding="utf-8")
    except OSError:
        return None


def strip_inline_comment(value: str) -> str:
    result: list[str] = []
    in_single = False
    in_double = False

    for char in value:
        if char == "'" and not in_double:
            in_single = not in_single
        elif char == '"' and not in_single:
            in_double = not in_double
        elif char == "#" and not in_single and not in_double:
            break
        result.append(char)

    return "".join(result).strip()


# Dots are allowed because config keys may use dotted names in future extensions,
# and the scanner is intentionally a little more permissive than the current file.
KEY_RE = re.compile(r"^(?P<indent>\s*)(?P<key>[A-Za-z0-9_.-]+):(?:\s*(?P<value>.*))?$")


def scan_yaml_like_keys(text: str) -> list[ConfigEntry]:
    stack: list[tuple[int, str]] = []
    entries: list[ConfigEntry] = []

    for line_no, raw_line in enumerate(text.splitlines(), start=1):
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#") or stripped.startswith("-"):
            continue

        match = KEY_RE.match(raw_line)
        if not match:
            continue

        indent = len(match.group("indent"))
        key = match.group("key")
        value = strip_inline_comment(match.group("value") or "")

        while stack and indent <= stack[-1][0]:
            stack.pop()

        stack.append((indent, key))
        entries.append(
            ConfigEntry(
                path=tuple(item[1] for item in stack),
                value=value,
                line_no=line_no,
                indent=indent,
            )
        )

    return entries


def config_values_by_path(entries: Iterable[ConfigEntry]) -> dict[tuple[str, ...], str]:
    return {entry.path: entry.value for entry in entries}


def child_keys(entries: Iterable[ConfigEntry], parent: tuple[str, ...]) -> set[str]:
    result: set[str] = set()
    target_depth = len(parent) + 1
    for entry in entries:
        if len(entry.path) == target_depth and entry.path[: len(parent)] == parent:
            result.add(entry.path[-1])
    return result


def get_section_lines(markdown_text: str, section_title: str) -> list[str]:
    lines = markdown_text.splitlines()
    start_pattern = re.compile(rf"^##\s+{re.escape(section_title)}\s*$", re.IGNORECASE)
    start = None
    for index, line in enumerate(lines):
        if start_pattern.match(line):
            start = index + 1
            break
    if start is None:
        return []

    result: list[str] = []
    for line in lines[start:]:
        if re.match(r"^##\s+", line):
            break
        result.append(line)
    return result


def extract_profile(summary_text: str, test_plan_text: str) -> str | None:
    summary_match = re.search(r"Definition of Done profile:\s*([a-z_]+)\s*-\s*met", summary_text, re.IGNORECASE)
    if summary_match:
        return summary_match.group(1).lower()

    test_plan_match = re.search(r"Profile \(from framework\.config\.yaml\):\s*([a-z_]+)", test_plan_text, re.IGNORECASE)
    if test_plan_match:
        return test_plan_match.group(1).lower()

    return None


def parse_profile_requirements(config_text: str, profile_name: str) -> dict[str, object]:
    entries = scan_yaml_like_keys(config_text)
    values = config_values_by_path(entries)
    prefix = ("definition_of_done", "profiles", profile_name)
    requirements: dict[str, object] = {}

    for path, value in values.items():
        if len(path) == len(prefix) + 1 and path[: len(prefix)] == prefix:
            key = path[-1]
            normalized = value.strip().strip('"')
            if normalized == "true":
                requirements[key] = True
            elif normalized == "false":
                requirements[key] = False
            elif normalized == "null":
                requirements[key] = None
            else:
                try:
                    requirements[key] = int(normalized)
                except ValueError:
                    try:
                        requirements[key] = float(normalized)
                    except ValueError:
                        requirements[key] = normalized

    return requirements


def parse_verification_cache(cache_text: str) -> dict[str, object]:
    work_item_id = None
    discovered_at = None
    commands: dict[str, str] = {}
    in_commands = False

    for line in cache_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("work_item_id:"):
            work_item_id = stripped.split(":", 1)[1].strip().strip('"')
        elif stripped.startswith("discovered_at:"):
            discovered_at = stripped.split(":", 1)[1].strip().strip('"')
        elif stripped == "commands:":
            in_commands = True
        elif in_commands:
            match = re.match(r"^\s+([a-z_]+):\s*\"?(.*?)\"?\s*$", line)
            if match:
                commands[match.group(1)] = match.group(2).strip()
            elif re.match(r"^\S", line) or re.match(r"^\s*[A-Za-z0-9_.-]+:\s*$", line):
                in_commands = False

    return {"work_item_id": work_item_id, "discovered_at": discovered_at, "commands": commands}


def parse_verification_steps(config_text: str) -> list[str]:
    lines = config_text.splitlines()
    steps: list[str] = []
    in_steps = False

    for line in lines:
        if not in_steps and re.match(r"^\s*steps:\s*$", line):
            in_steps = True
            continue
        if in_steps:
            match = re.match(r"^\s*-\s*([a-z_]+)\s*$", line)
            if match:
                steps.append(match.group(1))
                continue
            if re.match(r"^\s*[A-Za-z0-9_.-]+:\s*", line) or re.match(r"^\S", line):
                break

    return steps


def parse_verification_evidence(summary_text: str, test_plan_text: str) -> dict[str, str]:
    evidence: dict[str, str] = {}
    for line in get_section_lines(summary_text, "Verification Evidence"):
        match = re.match(r"^\s*-\s*([^:]+):\s*(.+?)\s*$", line)
        if match:
            evidence[match.group(1).strip().lower()] = match.group(2).strip()

    if not evidence:
        for line in get_section_lines(test_plan_text, "Verification Evidence"):
            match = re.match(r"^\s*-\s*([^:]+):\s*(.+?)\s*$", line)
            if match:
                evidence[match.group(1).strip().lower()] = match.group(2).strip()

    return evidence


def find_coverage_delta(text: str) -> float | None:
    match = re.search(r"Coverage delta[^:\n]*:\s*[^\d+-]*([+-]?\d+(?:\.\d+)?)", text, re.IGNORECASE)
    if not match:
        return None
    return float(match.group(1))


def evidence_lookup(evidence: dict[str, str], *keys: str) -> str | None:
    for key in keys:
        if key.lower() in evidence:
            return evidence[key.lower()]
    return None


def evidence_is_positive(value: str | None) -> bool:
    if not value:
        return False
    return bool(re.search(r"\b(clean|green|met|pass|passed|approved|yes|0 findings|0 problems|0 failed|none)\b", value, re.IGNORECASE))


def load_manifest_paths(manifest_path: Path) -> list[str]:
    manifest_text = read_text(manifest_path)
    if manifest_text is None:
        return []
    payload = json.loads(manifest_text)
    return list(payload.get("files", []))
