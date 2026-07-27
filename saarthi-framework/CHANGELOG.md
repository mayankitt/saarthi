# Changelog

All notable changes to the AI Agent Framework are documented here.
The format is loosely based on Keep a Changelog. Versions track `manifest.json`.

## [0.7.0] - 2026-07-27

Focus: KB auditor, capability-probe script, capability model aliases, and Saarthi observability log.

### Added
- `tools/audit_kb.py` — knowledge-base auditor: scans `knowledge-base/` for orphaned files (on disk but not in INDEX.md), dead links (in INDEX.md but missing on disk), preference files with missing or malformed YAML front-matter, and stale preferences (last_seen older than `preference_decay_days` from config). Supports `--stale-only` flag for quick staleness checks.
- `tools/run_capability_probe.py` — capability-probe execution script: reads `orchestration.capability_probe` dimensions and thresholds from `framework.config.yaml`, accepts per-dimension scores interactively or via `--scores dim=N,...`, computes a normalized score, and recommends the appropriate orchestration level (full/balanced/lean/minimal). Optionally writes `probe-result.yaml` via `--output`.
- `_framework/18-saarthi-observability.md` — lightweight per-work-item debug log design for Saarthi's own decisions: log location, entry format, canonical event names (`intake_started`, `mode_classified`, `probe_result`, `kb_hit`, `preference_applied`, `budget_alarm`, `gate_result`, `tool_invoked`, `orchestration_downgrade`, `work_item_closed`), when to emit, and privacy/sensitivity rules.
- `framework.config.yaml` — `models.capability_aliases` block mapping human-readable aliases (`fast`, `standard`, `reasoning`, `expert`) to tier keys (`tier_1_light` … `tier_4_specialist`).
- `framework.config.yaml` — `saarthi_observability` top-level block: `enabled`, `log_file`, `log_events`, `include_timestamps`, `redact_sensitive_values`.

### Changed
- `_framework/07-model-selection-policy.md` — added "Capability Aliases" section with an alias/tier/use-for table; renamed tier headings to include the alias (e.g. "Tier 1 — `fast`"); updated rules to prefer aliases in prose.
- `_framework/INDEX.md` — added row for 18 (Saarthi observability); updated intake load-on-demand note to include 18 and the capability probe tool.
- `tools/validate_framework.py` — added checks for `models.capability_aliases` (all four aliases declared and each resolves to a known tier) and `saarthi_observability` (required keys present).
- `tools/smoke_test_framework.py` — includes `tools/audit_kb.py` and `tools/run_capability_probe.py` in both the required-files check and the `--help` smoke run.
- `framework.config.schema.json` — added `saarthi_observability` to `required` and its property definition.
- `manifest.json` — bumped to `0.7.0`; added new files; updated notes.

### Preserved (intentionally unchanged in spirit)
- Agent-agnostic framework identity and operating model.
- Knowledge-base remains unseeded by default; audit script works on whatever content exists.
- Capability probe thresholds and dimensions are fully configurable via `framework.config.yaml`.



Focus: Python-first validation, schema/config hardening, and more concrete orchestration fallback behavior.

### Added
- `framework.config.schema.json` — editor-facing JSON Schema for the canonical control plane.
- `tools/framework_checks.py` — shared Python parsing and validation helpers for framework tooling.
- `tools/validate_work_item.py` — Python replacement for work-item validation with more deterministic evidence parsing from the `Verification Evidence` section.
- `tools/validate_framework.py` — framework/config validator that checks required files, schema JSON validity, config invariants, orchestration settings, and knowledge-base scaffolding.
- `tools/smoke_test_framework.py` — Python smoke test for the framework bundle.
- `tests/test_framework_validation.py` and `tests/test_policy_references.py` — automated tests for tool behavior, manifest integrity, and documented path references.
- `.github/workflows/framework-validation.yml` — repo CI that runs the smoke test, framework validator, and Python unit tests on Ubuntu and Windows.
- `framework.config.yaml` — new `orchestration` block for capability probing, orchestration levels, fallback order, and downgrade/escalation signals.
- `framework.config.yaml` — `adaptive_learning.runtime_enforcement` block for index lookup, staleness revalidation, citation requirements, contradiction capture, and silent-application limits.

### Changed
- Validation and smoke-test commands throughout the repo now prefer Python instead of Node.js.
- `framework.config.yaml` — added `cloud_balanced` and `local_medium` profiles plus an `ephemeral_task` budget entry.
- `_framework/15-multi-agent-orchestration.md` — replaced high-level prose with concrete orchestration levels, fallback strategies, pseudo-parallel execution guidance, and a synchronization contract.
- `_framework/16-adaptive-learning.md` — documented concrete runtime enforcement expectations for preference application and decay handling.
- `_framework/17-mcp-tool-discovery.md` — added machine-checkable hardening guidance for MCP registry entries.
- Publish scripts (`.sh`, `.zsh`, `.ps1`, `.bat`) now run Python-based validators/smoke tests.
- `README.md`, `AGENTS.md`, `SETUP-CHECKLIST.txt`, `saarthi.agent.md`, and related prompts/docs now point to Python tooling.

### Preserved (intentionally unchanged in spirit)
- Knowledge-base content remains unseeded by default; only the scaffolding and validation expectations were strengthened.
- Saarthi stays low-dependency and agent-agnostic.
- Work-item evidence and verification remain mandatory before any "done" claim.

## [0.5.0] - 2026-07-15

Focus: multi-tool installation, self-evolving framework, and MCP tool discovery.

### Added
- `_framework/16-adaptive-learning.md` — self-evolution policy: how the
  framework learns coding styles, workflow preferences, technology choices, and
  decision patterns from the user over time. Defines a confidence × criticality
  matrix that governs whether a learned preference is applied silently, surfaced
  as a default, or always confirmed (high-criticality decisions always require
  explicit user confirmation, regardless of confidence level).
- `_framework/17-mcp-tool-discovery.md` — MCP tool gap detection, registry
  research (modelcontextprotocol.io, mcp.so, GitHub), tool selection criteria,
  self-installation instructions per tool (VS Code, Cursor, Claude Code,
  Windsurf, and generic fallback), post-install verification, a pre-vetted tool
  catalog, and security/trust rules. Installation always requires user
  confirmation.
- `framework.config.yaml` — new `adaptive_learning` block with confidence
  thresholds (low→medium at 2 observations, medium→high at 3), preference decay
  days (90), always-confirm categories (security, auth, data-schema, infra,
  ci-cd), and auto-extract-at-finalization flag.
- `framework.config.yaml` — enhanced `mcp_servers` block with
  `discovery_registries`, `prefer_official`, and
  `require_user_confirmation_before_install` fields; added `package` field to
  the GitHub server entry.

### Changed
- `saarthi.agent.md` — made truly tool-agnostic: framework home resolution now
  lists concrete paths for GitHub Copilot (VS Code), Cursor, Claude Code,
  Windsurf/Cline/Continue, Antigravity, and a generic fallback. Intake now
  applies adaptive learning (16) and runs MCP capability check (17). Close step
  now triggers adaptive learning extraction. References to new policies 16 & 17
  added to framework binding and operating model.
- `saarthi-framework/SETUP-CHECKLIST.txt` — expanded from VS Code-only to cover
  all major tools: GitHub Copilot, Cursor, Claude Code (CLI), GitHub Copilot
  CLI, Windsurf, Cline/Continue, Antigravity/Antigravity CLI, and generic tools.
- `README.md` — added multi-tool installation guide section with per-tool steps
  for all supported tools; added 🧠 self-evolving and 🔌 MCP discovery to Key
  Features; updated directory structure to call out new framework files.
- `knowledge-base/preferences/README.md` — added structured preference record
  format (YAML front-matter with id, category, confidence, criticality, source,
  observed_count, last_seen, examples), application rules table, and reference
  to the full policy in `_framework/16-adaptive-learning.md`.
- `_framework/INDEX.md` — added rows for 16 (adaptive learning) and 17 (MCP
  discovery); updated load-on-demand order to include 16 at intake and finalize.
- `manifest.json` — bumped to `0.5.0`, updated description, added new files,
  expanded notes.

### Preserved (intentionally unchanged in spirit)
- Agent-agnostic `AGENTS.md` entry model.
- P0/P1/P2 question policy and budgets.
- Tiered ceremony philosophy and the six workflow modes.
- Compliance/audit-upfront stance.
- Execution-verification loop and evidence-backed DoD gates.
- Hard safety rules (always confirm before destructive/irreversible actions).

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
