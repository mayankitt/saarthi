# Multi-Agent Orchestration

The framework supports decomposing complex work items into specialized sub-tasks, but orchestration must degrade gracefully when the host agent or loaded model cannot support true parallel execution.

## 0. Capability Probe Before Orchestration

Before choosing an orchestration style, evaluate:

- host support for child/sub-agent spawning
- ability to preserve structured output across turns
- ability to follow contracts and handoffs
- ability to retain summarized context without reloading full history
- ability to complete the execution-verification loop reliably

Use the `orchestration.capability_probe` and `environment_profiles.*.preferred_orchestration_level` settings in `framework.config.yaml`.

## 1. Orchestration Levels

Choose the highest level the environment can support safely:

- **full** — full-history context, contract-first parallelism, broad lead participation
- **balanced** — moderate parallelism, summarized context, explicit integration checkpoints
- **lean** — sequential or pseudo-parallel execution, one active sub-task at a time, aggressive context trimming
- **minimal** — distilled mode, no parallelism, only essential gates and blocking questions

If capability signals degrade mid-task, downgrade one level and record the reason in `work-item-summary.md`.

## 2. When to Spawn Parallel Agents

True parallel agents are allowed only when all are true:

- the work has independent milestones with clear boundaries
- a sub-task contract exists before execution
- the host tool actually supports child agents
- the selected orchestration level allows parallelism
- the environment profile allows more than one active agent

Otherwise, use the fallback strategy below.

## 3. Work Breakdown Structure (WBS)

Before splitting work:

- identify boundaries (API schemas, interfaces, shared models, ownership rules)
- separate blocking tasks from parallelizable tasks
- define integration order
- define what each sub-task must produce to be considered complete

Do not split work if one branch is mostly waiting on another.

## 4. Sub-Task Contracts

Parallel or pseudo-parallel work always requires a contract:

- place contract definitions in `work-items/<WORK_ITEM_ID>/contracts/`
- define inputs, outputs, interfaces, error cases, and test ownership
- require each sub-task to explicitly state what is mocked, stubbed, or deferred

## 5. Context Isolation

- Each sub-task uses `work-items/<WORK_ITEM_ID>/sub-tasks/<SUB_ID>/`
- Pass only the sub-task requirement, local contract, and necessary shared decisions
- Do not force every sub-agent to read the full parent history unless necessary

## 6. Execution Strategy by Host Capability

### A. Native child-agent support

If the host supports child agents (for example Antigravity or a future host with first-class spawning), use the native mechanism.

### B. Limited host support

If the host supports multiple conversations but not true child control, use **pseudo-parallel orchestration**:

1. Create the WBS and contracts.
2. Execute one sub-task at a time using a standardized handoff block.
3. Persist each completed handoff in `work-items/<WORK_ITEM_ID>/sub-tasks/<SUB_ID>/`.
4. Resume the next sub-task from the saved contract + handoff instead of full history.

### C. No sub-agent support

Fall back to **role-collapsed orchestration**:

- keep the Domain Leads as internal reasoning roles only
- execute sub-tasks sequentially
- preserve boundaries with contracts and explicit "role output" blocks
- do not pretend true parallelism exists

## 7. Standardized Fallback Block

When native spawning is unavailable, use:

```text
[SUB-TASK HANDOFF]
Role: <Domain Lead / Worker Role>
Sub-Task ID: <SUB_ID>
Requirement: <Specific requirement>
Contract: work-items/<WORK_ITEM_ID>/contracts/<contract_name>.md
Depends On: <none | SUB_IDs>
Completion Criteria:
- <criterion>
Artifacts:
- work-items/<WORK_ITEM_ID>/sub-tasks/<SUB_ID>/summary.md
- work-items/<WORK_ITEM_ID>/sub-tasks/<SUB_ID>/status.yaml
```

## 8. Concrete Synchronization Plan

Every sub-task must produce:

- `summary.md` — what was done, decisions, open risks, evidence links
- `status.yaml` — `status`, `depends_on`, `ready_for_integration`, `blocked_by`, `updated_at`

The orchestrator integration loop is:

1. Create all planned sub-task contracts.
2. Mark each sub-task `planned`.
3. When a sub-task starts, mark it `in_progress`.
4. On completion, mark it `completed` and set `ready_for_integration: true/false`.
5. If a dependency fails or changes, mark affected sub-tasks `needs_replan`.
6. Integrate only when every required dependency is `completed`.
7. Run the full execution-verification loop (`13-execution-verification-loop.md`) after integration.

## 9. Guardrails

- Never claim parallelism if the host cannot support it.
- Never spawn without a contract.
- Never let sub-agents modify the same interface without a designated integration owner.
- If orchestration overhead exceeds expected benefit, collapse back to single-agent execution.
