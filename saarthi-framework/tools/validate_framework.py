#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from framework_checks import child_keys, config_values_by_path, parse_verification_steps, read_text, scan_yaml_like_keys


REQUIRED_TOP_LEVEL_KEYS = {
    "version",
    "agent_context",
    "environment_profiles",
    "orchestration",
    "mcp_servers",
    "adaptive_learning",
    "autonomy",
    "models",
    "workflow_modes",
    "budgets",
    "verification",
    "definition_of_done",
    "safety",
}

KNOWN_AGENTS = {
    "github_copilot",
    "claude_code",
    "cursor",
    "windsurf",
    "cline",
    "continue",
    "antigravity",
    "generic",
}

REQUIRED_KB_DIRS = [
    "architecture-decisions",
    "engineering-standards",
    "past-learnings",
    "preferences",
    "reusable-patterns",
]

REQUIRED_ORCHESTRATION_LEVELS = {"full", "balanced", "lean", "minimal"}


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate Saarthi framework structure and config invariants.")
    parser.add_argument("--root", "-r", default=".", help="Framework root (defaults to current directory)")
    return parser.parse_args(argv)


def emit(title: str, items: list[tuple[str, bool, str]]) -> None:
    print(f"\n{title}")
    for name, ok, detail in items:
        mark = "[PASS]" if ok else "[FAIL]"
        print(f"{mark} {name}: {detail}")


def validate_required_files(root: Path) -> list[tuple[str, bool, str]]:
    files = [
        "framework.config.yaml",
        "framework.config.schema.json",
        "_framework/INDEX.md",
        "tools/validate_work_item.py",
        "tools/smoke_test_framework.py",
    ]
    return [(path, (root / path).exists(), str(root / path)) for path in files]


def validate_json_schema(root: Path) -> list[tuple[str, bool, str]]:
    schema_path = root / "framework.config.schema.json"
    schema_text = read_text(schema_path)
    if schema_text is None:
        return [("schema file", False, f"Missing {schema_path}")]

    try:
        payload = json.loads(schema_text)
    except json.JSONDecodeError as exc:
        return [("schema json", False, f"{schema_path}: {exc}")]

    checks = [
        ("schema title", payload.get("title") == "Saarthi Framework Config", payload.get("title", "missing")),
        (
            "schema required top-level keys",
            REQUIRED_TOP_LEVEL_KEYS.issubset(set(payload.get("required", []))),
            ", ".join(payload.get("required", [])),
        ),
    ]
    return checks


def validate_config(root: Path) -> list[tuple[str, bool, str]]:
    config_path = root / "framework.config.yaml"
    config_text = read_text(config_path)
    if config_text is None:
        return [("framework.config.yaml", False, f"Missing {config_path}")]

    entries = scan_yaml_like_keys(config_text)
    values = config_values_by_path(entries)
    top_level = {path[0] for path in values if len(path) == 1}
    checks: list[tuple[str, bool, str]] = [
        (
            "top-level keys",
            REQUIRED_TOP_LEVEL_KEYS.issubset(top_level),
            f"Found: {', '.join(sorted(top_level))}",
        )
    ]

    known_agents = child_keys(entries, ("agent_context", "known_agents"))
    checks.append(("known agents catalog", known_agents == KNOWN_AGENTS, f"Found: {', '.join(sorted(known_agents))}"))

    active_agent = values.get(("agent_context", "active_agent"), "").strip('"')
    checks.append(("active_agent declared", active_agent in known_agents, active_agent or "missing"))

    profile_names = child_keys(entries, ("environment_profiles", "profiles"))
    active_profile = values.get(("environment_profiles", "active"), "").strip('"')
    checks.append(
        ("active environment profile", active_profile in profile_names, active_profile or "missing")
    )

    orchestration_levels = child_keys(entries, ("orchestration", "levels"))
    checks.append(
        (
            "orchestration levels",
            REQUIRED_ORCHESTRATION_LEVELS.issubset(orchestration_levels),
            f"Found: {', '.join(sorted(orchestration_levels))}",
        )
    )

    tier_map = child_keys(entries, ("models", "tier_map"))
    workflow_modes = child_keys(entries, ("workflow_modes",))
    dod_profiles = child_keys(entries, ("definition_of_done", "profiles"))
    budget_modes = child_keys(entries, ("budgets", "modes"))

    checks.append(("workflow modes declared", bool(workflow_modes), f"Found: {', '.join(sorted(workflow_modes))}"))
    checks.append(("DoD profiles declared", bool(dod_profiles), f"Found: {', '.join(sorted(dod_profiles))}"))

    for mode in sorted(workflow_modes):
        mode_path = ("workflow_modes", mode)
        model_tier = values.get(mode_path + ("model_tier",), "").strip('"')
        dod_profile = values.get(mode_path + ("dod_profile",), "").strip('"')
        checks.append((f"{mode}.model_tier", model_tier in tier_map, model_tier or "missing"))
        checks.append((f"{mode}.dod_profile", dod_profile in dod_profiles, dod_profile or "missing"))
        if mode != "ephemeral_task":
            checks.append((f"{mode} budget", mode in budget_modes, "present" if mode in budget_modes else "missing"))
        review_tier = values.get(mode_path + ("review_tier",), "").strip('"')
        if review_tier:
            checks.append((f"{mode}.review_tier", review_tier in tier_map, review_tier))

    adaptive_runtime_keys = child_keys(entries, ("adaptive_learning", "runtime_enforcement"))
    checks.append(
        (
            "adaptive runtime enforcement",
            {
                "require_index_lookup_at_intake",
                "revalidate_stale_preferences_at_intake",
                "require_citation_when_applying_preferences",
                "record_contradictions_in_summary",
            }.issubset(adaptive_runtime_keys),
            f"Found: {', '.join(sorted(adaptive_runtime_keys))}",
        )
    )

    capability_probe_keys = child_keys(entries, ("orchestration", "capability_probe"))
    checks.append(
        (
            "capability probe config",
            {"enabled", "probe_dimensions", "thresholds", "degrade_signals", "escalate_signals"}.issubset(capability_probe_keys),
            f"Found: {', '.join(sorted(capability_probe_keys))}",
        )
    )

    verification_steps = parse_verification_steps(config_text)
    checks.append(
        (
            "verification.discovery.steps",
            bool(verification_steps),
            ", ".join(verification_steps) if verification_steps else "missing",
        )
    )

    mcp_servers = child_keys(entries, ("mcp_servers", "servers"))
    checks.append(("MCP server registry", bool(mcp_servers), f"Found: {', '.join(sorted(mcp_servers))}"))
    for server in sorted(mcp_servers):
        server_path = ("mcp_servers", "servers", server)
        server_keys = child_keys(entries, server_path)
        checks.append(
            (
                f"mcp server {server}",
                {"expected_capabilities", "roles"}.issubset(server_keys),
                f"Found: {', '.join(sorted(server_keys))}",
            )
        )

    return checks


def validate_knowledge_base(root: Path) -> list[tuple[str, bool, str]]:
    checks: list[tuple[str, bool, str]] = []
    kb_root = root / "knowledge-base"
    index_path = kb_root / "INDEX.md"
    checks.append(("knowledge-base index", index_path.exists(), str(index_path)))
    for directory in REQUIRED_KB_DIRS:
        dir_path = kb_root / directory
        readme_path = dir_path / "README.md"
        checks.append((f"{directory} directory", dir_path.is_dir(), str(dir_path)))
        checks.append((f"{directory} README", readme_path.exists(), str(readme_path)))
    return checks


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    root = Path(args.root).resolve()

    sections = [
        ("Required files", validate_required_files(root)),
        ("Schema checks", validate_json_schema(root)),
        ("Config checks", validate_config(root)),
        ("Knowledge-base checks", validate_knowledge_base(root)),
    ]

    passed = True
    for title, items in sections:
        emit(title, items)
        passed = passed and all(ok for _, ok, _ in items)

    print("\nFRAMEWORK VALIDATION PASSED" if passed else "\nFRAMEWORK VALIDATION FAILED")
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
