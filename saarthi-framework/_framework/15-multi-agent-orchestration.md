# Multi-Agent Orchestration

The framework supports decomposing complex work items into parallel sub-tasks executed by specialized sub-agents. 

## When to Spawn Parallel Agents
- The task requires multiple non-overlapping skill sets (e.g., UI dev and Database migration).
- The task is large enough that a single agent's context window would be saturated.
- The `environment_profile` in `framework.config.yaml` allows `max_parallel_agents > 1`.

## 1. Work Breakdown Structure (WBS)
Before spawning agents, the orchestrator must create a breakdown of independent milestones.
- Identify the boundaries (e.g., API schemas, shared interfaces).
- Do not spawn parallel agents if one is strictly blocked by the other's implementation.

## 2. Sub-Task Contracts
To prevent deadlocks and merge conflicts, parallel agents must have a contract.
- Create a clear schema or interface definition before splitting work.
- Place contract definitions in `work-items/<WORK_ITEM_ID>/contracts/`.
- Sub-agents must mock or stub the other's implementation based on this contract until integration.

## 3. Context Isolation
- Each sub-agent operates in its own workspace: `work-items/<WORK_ITEM_ID>/sub-tasks/<SUB_ID>/`.
- Do not force sub-agents to read the entire parent `work-item-summary.md` if it contains irrelevant domain details.
- Provide them with only their specific sub-task requirement and the Sub-Task Contract.

## 4. Agent Spawning Mechanism (Environment Aware)
The orchestrator must use the host environment's native sub-agent invocation method.

**A. Antigravity (Google) Environment**
If you detect you are running inside Antigravity:
- Use the provided subagent tools (e.g., `invoke_subagent`, `browser_subagent`) directly to launch the parallel task.

**B. GitHub Copilot Workspace / Agent**
If you detect you are running inside a Copilot environment:
- Use the native `@workspace` or agent-slash commands to invoke child processes.

**C. Fallback (Generic Environment)**
If the environment is unknown, output a standardized block for the host application to parse:
```text
[SPAWN AGENT]
Role: <Domain Lead Role>
Sub-Task ID: <SUB_ID>
Requirement: <Specific requirement>
Context: work-items/<ID>/sub-tasks/<SUB_ID>/
Contract: work-items/<ID>/contracts/<contract_name>.md
```

## 5. Integration and Synchronization
- The Master Orchestrator pauses until all spawned sub-agents report completion.
- Once complete, the orchestrator runs the full Execution-Verification loop (`13-execution-verification-loop.md`) to ensure the integrated components work together.
