from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


FRAMEWORK_ROOT = Path(__file__).resolve().parents[1]


class FrameworkValidationTests(unittest.TestCase):
    def run_tool(self, relative_path: str, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(FRAMEWORK_ROOT / relative_path), *args],
            cwd=FRAMEWORK_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_smoke_test_passes(self) -> None:
        result = self.run_tool("tools/smoke_test_framework.py", "--root", str(FRAMEWORK_ROOT))
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)

    def test_framework_validator_passes(self) -> None:
        result = self.run_tool("tools/validate_framework.py", "--root", str(FRAMEWORK_ROOT))
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)

    def test_example_work_item_passes(self) -> None:
        result = self.run_tool(
            "tools/validate_work_item.py",
            "EXAMPLE-1001",
            "--root",
            str(FRAMEWORK_ROOT),
        )
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
