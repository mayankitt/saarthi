# सारथी (Saarthi) Framework MVP v0.3

A reusable, agent-agnostic software engineering operating model for individual developer productivity.

It supports:

- autonomous work item folder creation/resume
- strict no-guessing requirement clarification
- best-practice discovery questions
- workflow modes based on size/risk
- minimum viable ceremony
- model tier selection and reasoning budget control
- token optimization
- artifact-driven memory
- a machine-readable control plane (`framework.config.yaml`)
- an execution-verification loop with evidence-based, machine-checkable Definition of Done
- an autonomy dial (L1/L2/L3) with operational safety hard rules
- knowledge-base indexing for cheap, relevant retrieval
- security, compliance, audit logging, observability, QA, DevOps, and final learning extraction

## Start Here

Use:

```text
_framework/00-single-entry-prompt.md
```

or rely on root-level:

```text
AGENTS.md
```

if your AI coding assistant supports repository instructions.

For routing and the machine-readable control plane, see:

```text
_framework/INDEX.md
framework.config.yaml
```

A fully populated end-to-end example lives in `work-items/EXAMPLE-1001/`.

Before closing any work item, run:

```text
python tools/validate_work_item.py <WORK_ITEM_ID> --root .
```

and require a pass.

## Typical New Work Prompt

```text
Work Item ID: ABC-1234
Requirement: Admins should be able to assign roles to users.
```

## Typical Resume Prompt

```text
Resume ABC-1234
```

The assistant should infer:

```text
work-items/ABC-1234/
```

and read `work-item-summary.md` first.
