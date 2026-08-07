# Execution & Verification Loop

This is the missing half of the framework: **doing, verifying, and proving** —
not just planning. Planning produces specs; this phase produces *working,
proven* software. No work item is "done" without passing through this loop.

Source of truth for iteration limits and Definition of Done:
`framework.config.yaml` (`verification.*` and `definition_of_done.*`).

## Command Discovery (one-time per work item)

The framework is project-agnostic, so verification commands are **not**
hard-coded. On the **first** initialization of a work item, discover the
project's real commands and cache them once:

```text
work-items/<WORK_ITEM_ID>/verification-commands.yaml
```

Discovery procedure:

1. Inspect the project in the priority order listed under
   `verification.discovery.sources` in `framework.config.yaml` (package.json
   scripts, Makefile/Taskfile, pyproject/tox, gradle/maven, cargo/go/dotnet,
   CI config, README).
2. Resolve a command for each step (install, build, lint, typecheck,
   unit_tests, integration_tests, coverage, secret_scan). Leave a step empty if
   the project has none — empty means not-applicable/skipped, not failed.
3. Show the discovered set to the user once for confirmation
   (`confirm_with_user: true`), then write the cache file.
4. On every later turn, **read the cache** instead of re-discovering. Only
   refresh when tooling changes or a cached command no longer exists.

Use `templates/verification-commands.yaml` as the cache format.

## The Loop

```text
1. IMPLEMENT      Make the smallest correct change for the current slice.
2. RUN            Execute the relevant verification commands (build/lint/
                  typecheck/tests/coverage) from the work item's
                  verification-commands.yaml cache.
3. READ           Read the actual output. Parse failures; do not assume green.
4. DIAGNOSE       Identify the root cause of each failure.
5. FIX            Correct the cause (code or test), not the symptom.
6. REPEAT         Go to step 2 until all required checks are GREEN, or until
                  `verification.max_fix_iterations` is reached.
7. PROVE          Paste the final command output as gate evidence.
```

If `max_fix_iterations` is reached without green, **stop and report**: show the
remaining failures, your diagnosis, and the options. Do not loop indefinitely,
and do not silently disable or skip failing tests to force green.

## Evidence Is Mandatory

When `verification.evidence_required` is true (default), every gate that claims
a check passed MUST include the actual pasted command output (or a faithful
excerpt showing the result line). Self-reported "tests pass" without evidence
does not satisfy the gate.

Record evidence in `work-item-summary.md` under **Verification Evidence**.

Before claiming done, run the validator:

```text
python tools/validate_work_item.py <WORK_ITEM_ID> --root .
```

If it fails, the work item is not done.

Example evidence block:

```text
$ <unit_tests command>
... 142 passed, 0 failed, coverage 87.4% (+1.2%)

$ <lint command>
... 0 problems
```

## What "Run" Means by Step

| Step | Command key in cache | When |
|---|---|---|
| Build | `commands.build` | always (if defined) |
| Lint | `commands.lint` | always (if defined) |
| Typecheck | `commands.typecheck` | typed projects |
| Unit tests | `commands.unit_tests` | always when code changes |
| Integration tests | `commands.integration_tests` | cross-component changes |
| Coverage | `commands.coverage` | when DoD sets a coverage delta |
| Secret scan | `commands.secret_scan` | before release / strict DoD |

A command left empty in `verification-commands.yaml` is **not applicable** and is
skipped (not counted as a failure). If a project has no command for a required
check, ask the user for it rather than inventing one, then update the cache.

## Regression Is Required, Not Optional

Run the **existing** test suite, not only the new tests you added. A change that
breaks unrelated tests is not done. `regression_suite_green` in the
Definition-of-Done profile enforces this.

## Definition of Done (machine-checkable)

The current workflow mode maps to a `dod_profile` in `framework.config.yaml`.
A work item is done only when every required field in that profile is satisfied
**with evidence**. Empty/"n/a" commands are skipped, not failed.

`tools/validate_work_item.py` enforces this by checking:

- required artifacts exist (`work-item-summary.md`, `test-plan.md`, `verification-commands.yaml`)
- DoD profile is present
- required profile checks have evidence
- verification command cache keys are complete

Report the DoD as a checklist, e.g.:

```text
Definition of Done (profile: strict)
[x] build_passes              evidence: build output
[x] lint_clean                evidence: lint output
[x] typecheck_clean           evidence: typecheck output
[x] new_tests_required        added 6 tests
[x] regression_suite_green    142 passed
[x] coverage_delta_min_pct=1  +1.2%
[x] no_new_high_severity_findings
[x] self_review_passed        see self-review note
[x] security_gate_passed
[x] secret_scan_clean         0 findings
```

## Interaction With Autonomy

- **L1:** confirm before running tests / writing files.
- **L2 (default):** run the loop autonomously within the work item; checkpoint
  at phase boundaries; stop before irreversible actions.
- **L3:** run the loop end to end and report results; stop only on hard safety
  rules or budget thresholds.

See `14-autonomy-and-safety.md`.

## Anti-Patterns (do not do these)

- Claiming green without running the command.
- Deleting, skipping, or weakening failing tests to pass a gate.
- Fixing the test to match buggy code instead of fixing the code.
- Looping past `max_fix_iterations` instead of escalating.
- Using `--no-verify` or disabling checks to force a release.
