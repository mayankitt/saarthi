#!/usr/bin/env python3

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a lightweight Saarthi framework smoke test.")
    parser.add_argument("--root", "-r", default=".", help="Framework root (defaults to current directory)")
    return parser.parse_args(argv)


def print_checks(title: str, checks: list[tuple[str, bool, str]]) -> None:
    print(f"\n{title}")
    for name, ok, detail in checks:
        mark = "[PASS]" if ok else "[FAIL]"
        print(f"{mark} {name} -> {detail}")


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    root = Path(args.root).resolve()

    required_paths = [
        "framework.config.yaml",
        "framework.config.schema.json",
        "_framework/INDEX.md",
        "tools/validate_work_item.py",
        "tools/validate_framework.py",
        "tools/audit_kb.py",
        "tools/run_capability_probe.py",
    ]
    checks = []
    for rel_path in required_paths:
        full_path = root / rel_path
        checks.append((rel_path, full_path.exists(), str(full_path)))
    print_checks("Smoke test: required files", checks)
    ok = all(item[1] for item in checks)

    for tool_rel_path in (
        "tools/validate_work_item.py",
        "tools/validate_framework.py",
        "tools/audit_kb.py",
        "tools/run_capability_probe.py",
    ):
        tool_path = root / tool_rel_path
        if not tool_path.exists():
            ok = False
            continue
        result = subprocess.run(
            [sys.executable, str(tool_path), "--help"],
            capture_output=True,
            text=True,
            check=False,
        )
        help_ok = result.returncode == 0
        print(f"\nSmoke test: {tool_rel_path} --help")
        print(f"{'[PASS]' if help_ok else '[FAIL]'} {sys.executable} {tool_rel_path} --help")
        if not help_ok:
            if result.stdout.strip():
                print(result.stdout.strip())
            if result.stderr.strip():
                print(result.stderr.strip())
        ok = ok and help_ok

    print(f"\n{'SMOKE TEST PASSED' if ok else 'SMOKE TEST FAILED'}")
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
