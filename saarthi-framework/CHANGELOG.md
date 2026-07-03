# Changelog

All notable changes to the AI Agent Framework are documented here.
The format is loosely based on Keep a Changelog. Versions track `manifest.json`.

## [0.4.0] - 2026-06-30

Focus: close the execution-verification gap and make governance machine-checkable
without losing the planning/governance intent of v0.3.

### Added
- `framework.config.yaml` — machine-readable control plane and single source of
  truth for workflow modes, model tier mapping, token/cost budgets with
  stop-and-report thresholds, machine-checkable Definition of Done, and hard
  safety rules.
- `_framework/INDEX.md` — router mapping decisions to their canonical source,
  plus an always-on minimal core to fight instruction-adherence drift under load.
- `_framework/13-execution-verification-loop.md` — first-class
  act -> run build/test/lint -> read failures -> fix -> repeat-until-green phase,
  with mandatory pasted command output as gate evidence.
- `_framework/14-autonomy-and-safety.md` — autonomy dial (L1/L2/L3), a decision
  register for after-the-fact human audit, and operational safety hard rules
  (irreversible actions, secret handling, auth/authz protection).
- `tools/validate-work-item.js` — zero-dependency Node validator that enforces
  evidence-backed DoD checks and verification cache integrity per work item.
- `knowledge-base/INDEX.md` — retrieval manifest so agents load only relevant
  preferences/patterns/ADRs instead of reading the whole knowledge base.
- A fully populated few-shot example under `work-items/_example-work-item/` to
  anchor output quality and consistency.
- `templates/verification-commands.yaml` — cache format for the one-time,
  per-work-item verification command discovery.

### Changed
- `framework.config.yaml` — `models.selection: auto` lets the orchestrator pick
  the appropriate model per tier (tier_map values become preferred hints).
  Verification commands are no longer hard-coded; they are auto-discovered once
  per work item and cached in `work-items/<ID>/verification-commands.yaml`.
- `_framework/05-quality-gates.md` — gates now require verification evidence, a
  machine-checkable Definition of Done, a mandatory self-review gate, a
  regression (existing-suite) run, and a secret scan.
- `_framework/05-quality-gates.md`, `_framework/13-execution-verification-loop.md`, and
  `AGENTS.md` now require running `node tools/validate-work-item.js <WORK_ITEM_ID>`
  before any final "done" claim.
- `_framework/02-workflow-modes.md`, `_framework/07-model-selection-policy.md` —
  now reference `framework.config.yaml` as the source of truth.
- `templates/work-item-summary.md` — added a Decision/Assumption Register and a
  Verification Evidence section.
- `templates/test-plan.md`, `templates/security-review.md` — added regression and
  Definition-of-Done evidence / secret-scan fields.
- De-duplicated Strict Mode and work-item lifecycle restatements across
  `AGENTS.md`, `00`, `01`, and `12` into canonical sources plus thin pointers.
- `manifest.json` bumped to `0.4.0` with the new files registered.

### Preserved (intentionally unchanged in spirit)
- Agent-agnostic `AGENTS.md` entry model.
- P0/P1/P2 question policy and budgets.
- Tiered ceremony philosophy and the six workflow modes.
- Compliance/audit-upfront stance.
- Learning-extraction -> knowledge-base closing loop.

## [0.3.0] - prior

- Initial MVP: AGENTS.md entry, master orchestrator, workflow modes, question
  policy, agent registry, quality gates, token/model/reasoning policies,
  lifecycle + finalize prompts, templates, and knowledge-base scaffolding.
