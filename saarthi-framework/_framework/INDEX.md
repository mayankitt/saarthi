# Framework Index / Router

This file maps **decisions to their governing source**. Read this first to know
which file owns a rule, so you load only what you need (token discipline).

> **Distilled Mode / Local Small:** If `environment_profiles.active` is `local_small`, STOP READING THIS FILE. Immediately route to `_framework/00a-distilled-entry-prompt.txt` and ignore all other framework orchestration files to prevent cognitive overload.

## Canonical sources (one owner per concern)

| Decision / concern | Canonical source |
|---|---|
| Machine-readable modes, tiers, budgets, DoD, safety | `framework.config.yaml` |
| **Host coding agent identity & compatibility** | **`framework.config.yaml` → `agent_context`** |
| Entry behavior + output format | `_framework/00-single-entry-prompt.md` |
| Orchestration, routing, classification | `_framework/01-saarthi-orchestrator.md` |
| Workflow mode definitions (prose) | `_framework/02-workflow-modes.md` |
| Question prioritization (P0/P1/P2) + budgets | `_framework/03-question-policy.md` |
| Agent roster + consultation style | `_framework/04-agent-registry.md` |
| Quality gates + evidence requirements | `_framework/05-quality-gates.md` |
| Token optimization | `_framework/06-token-optimization-policy.md` |
| Model tier selection (prose) | `_framework/07-model-selection-policy.md` |
| Reasoning budget | `_framework/08-reasoning-budget-policy.md` |
| Resume behavior | `_framework/09-resume-work-item-prompt.md` |
| Finalize + learning extraction | `_framework/10-finalize-work-item-prompt.md` |
| Minimum viable ceremony | `_framework/11-minimum-viable-ceremony.md` |
| Work item lifecycle | `_framework/12-work-item-lifecycle-policy.md` |
| **Execution & verification loop (do/verify/prove)** | `_framework/13-execution-verification-loop.md` |
| **Autonomy dial + operational safety** | `_framework/14-autonomy-and-safety.md` |
| **Multi-agent execution + spawning + fallback levels** | `_framework/15-multi-agent-orchestration.md` |
| **Adaptive learning + self-evolution** | `_framework/16-adaptive-learning.md` |
| **MCP tool discovery + self-install** | `_framework/17-mcp-tool-discovery.md` |
| **Saarthi observability & debug log** | `_framework/18-saarthi-observability.md` |
| Knowledge-base retrieval | `knowledge-base/INDEX.md` |

When prose disagrees with `framework.config.yaml`, the config wins.

## Adherence under load (always-on minimal core)

Instruction adherence degrades as context grows. Keep this minimal core in
mind at all times; load deeper docs only when the current phase needs them.

1. **Strict Mode by default** — do not invent requirements, rules, or behavior.
2. **Lightest safe ceremony** — pick the smallest workflow mode that protects
   correctness, security, compliance, observability, testability, and UX.
3. **Implement, then verify with evidence** — every "done" claim is backed by
   pasted build/test/lint output (see 13). No self-reported green.
4. **Respect hard safety rules** — never bypass `safety.always_confirm_before`
   in `framework.config.yaml`, regardless of autonomy level.
5. **Keep `work-item-summary.md` current** — it is compressed memory.

Everything else is detail to load on demand via this index.

## Load-on-demand order (per phase)

- **Intake/clarification:** 00, 03, 11, 12, 16 (apply known preferences), 18 (start debug log) + `knowledge-base/INDEX.md` + `agent_context` from `framework.config.yaml` (load host agent identity for tool discovery qualification)
- **Orchestration selection:** 15 + `environment_profiles` and `orchestration` from `framework.config.yaml`; optionally run capability probe (tools/run_capability_probe.py) and emit `probe_result` event
- **Design:** 01, 02, 04, 05 (design gate), 07, 08
- **Development:** 13, 14, 05 (dev gate), `framework.config.yaml` verification
- **QA/Release:** 05 (release gate), 13 (evidence), test-plan artifact
- **Finalize:** 10 + 16 (capture new preferences) + knowledge-base
