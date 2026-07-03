# Resume Work Item Prompt

Resume work item: `<WORK_ITEM_ID>`

Automatically use folder:

```text
work-items/<WORK_ITEM_ID>/
```

First read:

```text
work-items/<WORK_ITEM_ID>/work-item-summary.md
```

Then read only relevant available artifacts.

Do not restart from scratch.

## Context Loading Order

1. work-item-summary.md
2. clarification-log.md if unresolved questions exist
3. current phase artifact
4. design-spec.md if implementation/testing is ongoing
5. implementation-plan.md if development is ongoing
6. test-plan.md if QA is ongoing
7. security-review.md, audit-compliance-review.md, observability-plan.md only when relevant

## Output Format

```markdown
## Resume Summary

### Current Phase
<phase>

### Completed
- <item>

### In Progress
- <item>

### Blocked
- <item>

### Important Decisions So Far
- <decision>

### Risks
- <risk>

### Next Recommended Step
<step>

### Questions
#### P0 - Blocking
<questions or "None">

#### P1 - Recommended
<questions or "None">

#### P2 - Optional
<questions or "None">
```
