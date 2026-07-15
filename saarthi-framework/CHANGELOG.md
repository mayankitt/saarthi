# Changelog

All notable changes to the AI Agent Framework are documented here.
The format is loosely based on Keep a Changelog. Versions track `manifest.json`.

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
