#!/usr/bin/env python3
"""Capability probe execution script for the Saarthi framework.

Reads the ``orchestration.capability_probe`` configuration block and evaluates
the current model's capability score across all defined dimensions.  The score
determines the recommended orchestration level (full / balanced / lean / minimal).

Two input modes:
  Interactive (default) — prompts for a 0-100 score for each dimension.
  Non-interactive        — pass ``--scores dim1=N,dim2=N,...`` on the command line.

Output:
  - Prints dimension breakdown and final recommendation to stdout.
  - Optionally writes a ``probe-result.yaml`` file (use ``--output <path>``).

Usage:
    python tools/run_capability_probe.py --root saarthi-framework
    python tools/run_capability_probe.py --root saarthi-framework \\
        --scores structured_output=18,multi_step_follow_through=15,\\
                 tool_recall=12,verification_discipline=14,\\
                 context_retention=13,parallel_coordination=10
    python tools/run_capability_probe.py --root saarthi-framework \\
        --scores structured_output=18,multi_step_follow_through=15 \\
        --output work-items/MY-WORK-ITEM/probe-result.yaml
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

from framework_checks import read_text, scan_yaml_like_keys, config_values_by_path, child_keys


# ---------------------------------------------------------------------------
# Config loading
# ---------------------------------------------------------------------------

def load_probe_config(root: Path) -> dict:
    """Parse orchestration.capability_probe from framework.config.yaml."""
    config_text = read_text(root / "framework.config.yaml")
    if config_text is None:
        raise FileNotFoundError(f"framework.config.yaml not found in {root}")

    entries = scan_yaml_like_keys(config_text)
    values = config_values_by_path(entries)

    # Probe dimensions: key → max_weight
    dim_keys = child_keys(entries, ("orchestration", "capability_probe", "probe_dimensions"))
    dimensions: dict[str, int] = {}
    for dim in dim_keys:
        raw = values.get(("orchestration", "capability_probe", "probe_dimensions", dim), "0")
        try:
            dimensions[dim] = int(raw.strip().strip('"'))
        except ValueError:
            dimensions[dim] = 0

    # Thresholds: level → minimum score
    threshold_keys = child_keys(entries, ("orchestration", "capability_probe", "thresholds"))
    thresholds: dict[str, int] = {}
    for level in threshold_keys:
        raw = values.get(("orchestration", "capability_probe", "thresholds", level), "0")
        try:
            thresholds[level] = int(raw.strip().strip('"'))
        except ValueError:
            thresholds[level] = 0

    # Degrade / escalate signals (list items, parsed from raw config text)
    degrade_signals = _parse_list_under(config_text, "degrade_signals")
    escalate_signals = _parse_list_under(config_text, "escalate_signals")

    return {
        "dimensions": dimensions,
        "thresholds": thresholds,
        "degrade_signals": degrade_signals,
        "escalate_signals": escalate_signals,
    }


def _parse_list_under(config_text: str, key: str) -> list[str]:
    """Naive extraction of YAML list items under a given key name."""
    items: list[str] = []
    in_section = False
    for line in config_text.splitlines():
        stripped = line.strip()
        if stripped == f"{key}:":
            in_section = True
            continue
        if in_section:
            if stripped.startswith("- "):
                items.append(stripped[2:].strip().strip('"'))
            elif stripped and not stripped.startswith("#"):
                # Another top-level or same-level key encountered
                in_section = False
    return items


# ---------------------------------------------------------------------------
# Score input
# ---------------------------------------------------------------------------

def parse_scores_arg(raw: str, dimensions: dict[str, int]) -> dict[str, float]:
    """Parse ``dim=N,dim=N`` string into a score dict."""
    scores: dict[str, float] = {}
    for pair in raw.split(","):
        pair = pair.strip()
        if "=" not in pair:
            continue
        dim, _, val = pair.partition("=")
        dim = dim.strip()
        try:
            scores[dim.strip()] = float(val.strip())
        except ValueError:
            pass
    return scores


def prompt_scores(dimensions: dict[str, int]) -> dict[str, float]:
    """Interactively ask the user to score each dimension."""
    print("\n=== Capability Probe — Score Entry ===")
    print("For each dimension, enter a raw score from 0 to its maximum weight.")
    print("Enter '?' for guidance on what each dimension tests.\n")
    guidance = {
        "structured_output": "Does the model consistently emit all required response sections in the correct format?",
        "multi_step_follow_through": "Can the model complete a multi-step plan without losing track of earlier steps?",
        "tool_recall": "Does the model remember and correctly reuse tools, commands, and findings across turns?",
        "verification_discipline": "Does the model run verification commands and cite evidence rather than self-reporting?",
        "context_retention": "Can the model work from summaries/contracts without reloading the full conversation history?",
        "parallel_coordination": "Can the model manage parallel or pseudo-parallel sub-tasks without boundary confusion?",
    }
    scores: dict[str, float] = {}
    for dim, max_weight in dimensions.items():
        while True:
            raw = input(f"  {dim} (0-{max_weight}): ").strip()
            if raw == "?":
                print(f"    → {guidance.get(dim, 'No guidance available.')}")
                continue
            try:
                val = float(raw)
                if 0.0 <= val <= max_weight:
                    scores[dim] = val
                    break
                print(f"    Must be between 0 and {max_weight}.")
            except ValueError:
                print("    Please enter a number.")
    return scores


# ---------------------------------------------------------------------------
# Scoring engine
# ---------------------------------------------------------------------------

LEVEL_ORDER = ["full", "balanced", "lean", "minimal"]


def compute_result(
    scores: dict[str, float],
    dimensions: dict[str, int],
    thresholds: dict[str, int],
) -> dict:
    """Return dimension breakdown, total score, and recommended level."""
    total_weight = sum(dimensions.values())
    total_score = 0.0
    breakdown: list[dict] = []

    for dim, max_weight in dimensions.items():
        raw = scores.get(dim, 0.0)
        # Clamp
        raw = max(0.0, min(float(max_weight), raw))
        pct = (raw / max_weight * 100) if max_weight else 0.0
        total_score += raw
        breakdown.append(
            {
                "dimension": dim,
                "score": raw,
                "max": max_weight,
                "pct": round(pct, 1),
            }
        )

    # Normalize to 0-100
    normalized = (total_score / total_weight * 100) if total_weight else 0.0

    # Map to orchestration level (highest threshold the score meets)
    recommended = "minimal"
    for level in LEVEL_ORDER:
        if normalized >= thresholds.get(level, 0):
            recommended = level
            break

    return {
        "breakdown": breakdown,
        "total_score": round(total_score, 1),
        "total_weight": total_weight,
        "normalized_pct": round(normalized, 1),
        "recommended_level": recommended,
        "thresholds": thresholds,
    }


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def print_result(result: dict, degrade: list[str], escalate: list[str]) -> None:
    print("\n=== Capability Probe Results ===\n")
    print(f"{'Dimension':<35} {'Score':>7} {'Max':>5} {'%':>6}")
    print("-" * 57)
    for row in result["breakdown"]:
        bar_filled = int(row["pct"] / 5)
        bar = "█" * bar_filled + "░" * (20 - bar_filled)
        print(f"  {row['dimension']:<33} {row['score']:>6.1f} {row['max']:>5}  {bar}  {row['pct']:>5.1f}%")
    print("-" * 57)
    print(f"  {'TOTAL':<33} {result['total_score']:>6.1f} {result['total_weight']:>5}")
    print(f"\n  Normalized score : {result['normalized_pct']:.1f} / 100")

    print("\n  Thresholds:")
    for level in LEVEL_ORDER:
        thresh = result["thresholds"].get(level, 0)
        marker = " ◄ recommended" if level == result["recommended_level"] else ""
        print(f"    {level:<12} ≥ {thresh:>3}{marker}")

    print(f"\n  ✓ Recommended orchestration level: {result['recommended_level'].upper()}")

    if degrade:
        print("\n  Watch for degrade signals (drop a level if observed):")
        for s in degrade:
            print(f"    - {s}")
    if escalate:
        print("\n  Watch for escalate signals (raise a level if sustained):")
        for s in escalate:
            print(f"    - {s}")


def write_yaml_result(output_path: Path, result: dict) -> None:
    """Write a probe-result.yaml file."""
    timestamp = datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    lines = [
        "# Saarthi capability probe result",
        f"# Generated: {timestamp}",
        "",
        f"recommended_level: {result['recommended_level']}",
        f"normalized_score_pct: {result['normalized_pct']}",
        f"total_score: {result['total_score']}",
        f"total_weight: {result['total_weight']}",
        f"generated_at: \"{timestamp}\"",
        "",
        "dimension_scores:",
    ]
    for row in result["breakdown"]:
        lines.append(f"  {row['dimension']}: {row['score']}  # max {row['max']} ({row['pct']}%)")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\n  Probe result written to: {output_path}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Run the Saarthi capability probe to determine the recommended "
            "orchestration level for the current model/environment."
        )
    )
    parser.add_argument(
        "--root", "-r", default=".", help="Framework root directory (default: current directory)"
    )
    parser.add_argument(
        "--scores",
        default="",
        help=(
            "Comma-separated dimension=score pairs, e.g. "
            "structured_output=18,tool_recall=12. "
            "Omit to enter scores interactively."
        ),
    )
    parser.add_argument(
        "--output",
        default="",
        help="Optional path to write probe-result.yaml (e.g. work-items/MY-ID/probe-result.yaml).",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    root = Path(args.root).resolve()

    try:
        probe_cfg = load_probe_config(root)
    except FileNotFoundError as exc:
        print(f"[ERROR] {exc}")
        return 2

    dimensions = probe_cfg["dimensions"]
    if not dimensions:
        print("[ERROR] No probe_dimensions found in orchestration.capability_probe config.")
        return 2

    # Collect scores
    if args.scores:
        scores = parse_scores_arg(args.scores, dimensions)
        # Fill missing dimensions with 0
        for dim in dimensions:
            scores.setdefault(dim, 0.0)
    else:
        try:
            scores = prompt_scores(dimensions)
        except (EOFError, KeyboardInterrupt):
            print("\n[ABORTED] Probe cancelled.")
            return 1

    result = compute_result(scores, dimensions, probe_cfg["thresholds"])
    print_result(result, probe_cfg["degrade_signals"], probe_cfg["escalate_signals"])

    if args.output:
        write_yaml_result(Path(args.output), result)

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
