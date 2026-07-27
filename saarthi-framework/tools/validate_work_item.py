#!/usr/bin/env python3

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from framework_checks import (
    evidence_is_positive,
    evidence_lookup,
    extract_profile,
    find_coverage_delta,
    parse_profile_requirements,
    parse_verification_cache,
    parse_verification_evidence,
    parse_verification_steps,
    read_text,
)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate a Saarthi work item against the configured Definition of Done."
    )
    parser.add_argument("work_item_id", nargs="?", help="Work item ID to validate")
    parser.add_argument("--work-item", "-w", dest="work_item_flag", help="Work item ID to validate")
    parser.add_argument("--root", "-r", default=".", help="Framework root (defaults to current directory)")
    args = parser.parse_args(argv)
    args.work_item = args.work_item_flag or args.work_item_id
    if not args.work_item:
        parser.print_usage(sys.stderr)
        raise SystemExit(64)
    return args


def validate_requirement(
    key: str,
    required_value: object,
    evidence: dict[str, str],
    combined_text: str,
) -> tuple[bool, str]:
    if required_value in (False, None):
        return True, f"{key} is not required by this profile"

    if key == "build_passes":
        value = evidence_lookup(evidence, "build")
        return evidence_is_positive(value), f"Build evidence: {value or 'missing'}"

    if key == "lint_clean":
        value = evidence_lookup(evidence, "lint", "lint / typecheck")
        return evidence_is_positive(value), f"Lint evidence: {value or 'missing'}"

    if key == "typecheck_clean":
        value = evidence_lookup(evidence, "typecheck", "lint / typecheck")
        return evidence_is_positive(value), f"Typecheck evidence: {value or 'missing'}"

    if key == "new_tests_required":
        value = evidence_lookup(evidence, "unit tests")
        ok = bool(value and ("new" in value.lower() or evidence_is_positive(value)))
        return ok, f"New test evidence: {value or 'missing'}"

    if key == "regression_suite_green":
        value = evidence_lookup(evidence, "regression (existing suite)", "regression")
        return evidence_is_positive(value), f"Regression evidence: {value or 'missing'}"

    if key == "no_new_high_severity_findings":
        value = evidence_lookup(evidence, "high severity findings", "high-severity findings")
        if value is None:
            value = "yes" if re_search(r"\b(no new high[- ]severity findings|0 high[- ]severity findings|none)\b", combined_text) else None
        return evidence_is_positive(value), f"High-severity findings evidence: {value or 'missing'}"

    if key == "self_review_passed":
        value = evidence_lookup(evidence, "self-review", "self review")
        if value is None:
            value = "pass" if re_search(r"\bself[- ]review\b.*\b(pass|passed|approved)\b", combined_text) else None
        return evidence_is_positive(value), f"Self-review evidence: {value or 'missing'}"

    if key == "security_gate_passed":
        value = evidence_lookup(evidence, "security gate", "security recommendation")
        if value is None:
            value = "pass" if re_search(r"\bsecurity gate\b.*\b(pass|passed|approved)\b", combined_text) else None
        return evidence_is_positive(value), f"Security gate evidence: {value or 'missing'}"

    if key == "secret_scan_clean":
        value = evidence_lookup(evidence, "secret scan")
        return evidence_is_positive(value), f"Secret scan evidence: {value or 'missing'}"

    if key == "assumptions_documented":
        ok = re_search(r"decision\s*/\s*assumption register|assumptions?", combined_text)
        return ok, "Assumptions documented" if ok else "Assumptions not documented"

    if key == "coverage_delta_min_pct":
        evidence_value = evidence_lookup(evidence, "coverage delta")
        delta = find_coverage_delta(evidence_value or combined_text)
        if delta is None:
            return False, f"Coverage delta missing (expected >= {required_value})"
        return delta >= float(required_value), f"Coverage delta {delta} >= {required_value}"

    return True, f"{key} not currently validated by script"


def re_search(pattern: str, text: str) -> bool:
    import re

    return bool(re.search(pattern, text, re.IGNORECASE))


def print_result(title: str, items: list[tuple[str, bool, str]]) -> None:
    print(f"\n{title}")
    for name, ok, note in items:
        mark = "[PASS]" if ok else "[FAIL]"
        print(f"{mark} {name}: {note}")


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    root = Path(args.root).resolve()
    work_item_id = args.work_item

    config_path = root / "framework.config.yaml"
    item_dir = root / "work-items" / work_item_id
    summary_path = item_dir / "work-item-summary.md"
    test_plan_path = item_dir / "test-plan.md"
    cache_path = item_dir / "verification-commands.yaml"

    config_text = read_text(config_path)
    summary_text = read_text(summary_path)
    test_plan_text = read_text(test_plan_path)
    cache_text = read_text(cache_path)

    file_checks = [
        ("framework.config.yaml", config_text is not None, str(config_path) if config_text else f"Missing {config_path}"),
        ("work-item-summary.md", summary_text is not None, str(summary_path) if summary_text else f"Missing {summary_path}"),
        ("test-plan.md", test_plan_text is not None, str(test_plan_path) if test_plan_text else f"Missing {test_plan_path}"),
        (
            "verification-commands.yaml",
            cache_text is not None,
            str(cache_path) if cache_text else f"Missing {cache_path}",
        ),
    ]
    print_result("File checks", file_checks)
    if any(not ok for _, ok, _ in file_checks):
        return 2

    profile = extract_profile(summary_text, test_plan_text)
    profile_checks = [("DoD profile", profile is not None, f"Profile '{profile}' detected" if profile else "Could not determine DoD profile")]
    print_result("DoD profile", profile_checks)
    if profile is None:
        return 2

    requirements = parse_profile_requirements(config_text, profile)
    if not requirements:
        print("\n[FAIL] Could not parse Definition of Done requirements from framework.config.yaml")
        return 2

    cache = parse_verification_cache(cache_text)
    expected_steps = parse_verification_steps(config_text)
    cache_checks: list[tuple[str, bool, str]] = [
        (
            "cache work_item_id",
            cache["work_item_id"] == work_item_id,
            f"Found '{cache['work_item_id']}'" if cache["work_item_id"] else "Missing work_item_id",
        ),
        (
            "cache discovered_at",
            bool(cache["discovered_at"]),
            str(cache["discovered_at"] or "Missing discovered_at"),
        ),
    ]

    commands = cache["commands"]
    for step in expected_steps:
        exists = step in commands
        value = commands.get(step, "")
        cache_checks.append(
            (
                f"cache commands.{step}",
                exists,
                f"Present ({'set' if value else 'empty/not-applicable'})" if exists else "Missing key",
            )
        )

    has_command = any(value for value in commands.values())
    cache_checks.append(("cache has at least one executable command", has_command, "Yes" if has_command else "All commands empty"))
    print_result("Verification command cache", cache_checks)

    evidence = parse_verification_evidence(summary_text, test_plan_text)
    combined_text = "\n".join([summary_text, test_plan_text])
    requirement_checks = []
    for key, required_value in requirements.items():
        ok, note = validate_requirement(key, required_value, evidence, combined_text)
        requirement_checks.append((key, ok, note))

    print_result(f"Definition of Done checks ({profile})", requirement_checks)

    passed = all(ok for _, ok, _ in file_checks + profile_checks + cache_checks + requirement_checks)
    print("\nVALIDATION PASSED" if passed else "\nVALIDATION FAILED")
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
