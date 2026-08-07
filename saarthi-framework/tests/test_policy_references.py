from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
FRAMEWORK_ROOT = REPO_ROOT / "saarthi-framework"
PATH_PATTERN = re.compile(
    # Framework-relative file references that should resolve from either the repo
    # root or the framework root depending on where they are documented.
    r"(?P<path>(?:saarthi-framework[\\/])?(?:_framework|knowledge-base|templates|tools|work-items)[\\/][A-Za-z0-9._\\/\-]+\.[A-Za-z0-9._-]+|"
    r"(?:saarthi-framework[\\/])?framework\.config(?:\.schema)?\.json|"
    r"(?:saarthi-framework[\\/])?framework\.config\.yaml|"
    r"(?:saarthi-framework[\\/])?AGENTS\.md|"
    r"(?:saarthi-framework[\\/])?SETUP-CHECKLIST\.txt)"
)


def candidate_targets(current_file: Path, raw_path: str) -> list[Path]:
    targets = [current_file.parent / raw_path]
    if raw_path.startswith("saarthi-framework/"):
        targets.append(REPO_ROOT / raw_path)
    else:
        targets.append(FRAMEWORK_ROOT / raw_path)
        targets.append(REPO_ROOT / raw_path)
    deduped = []
    seen = set()
    for target in targets:
        resolved = target.resolve()
        if resolved not in seen:
            deduped.append(resolved)
            seen.add(resolved)
    return deduped


class PolicyReferenceTests(unittest.TestCase):
    def iter_files(self) -> list[Path]:
        globs = ["*.md", "*.txt", "*.json", "*.yaml", "*.yml", "*.ps1", "*.sh", "*.bat"]
        files: list[Path] = []
        for pattern in globs:
            files.extend(REPO_ROOT.rglob(pattern))
        return [path for path in files if ".git" not in path.parts and "__pycache__" not in path.parts]

    def test_documented_paths_exist(self) -> None:
        missing: list[str] = []
        for file_path in self.iter_files():
            text = file_path.read_text(encoding="utf-8")
            for match in PATH_PATTERN.finditer(text):
                raw_path = match.group("path").rstrip(".,)")
                if raw_path.startswith("work-items/") and re.search(r"work-items/[A-Z]+-\d+/", raw_path):
                    continue
                if not any(target.exists() for target in candidate_targets(file_path, raw_path)):
                    missing.append(f"{file_path}: {raw_path}")
        self.assertFalse(missing, "\n".join(missing))

    def test_manifest_paths_exist(self) -> None:
        manifest = json.loads((FRAMEWORK_ROOT / "manifest.json").read_text(encoding="utf-8"))
        missing = [entry for entry in manifest.get("files", []) if not (FRAMEWORK_ROOT / entry).exists()]
        self.assertFalse(missing, f"Missing manifest entries: {missing}")


if __name__ == "__main__":
    unittest.main()
