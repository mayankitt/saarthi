# Finalize Work Item Prompt

Finalize work item: `<WORK_ITEM_ID>`

Automatically use folder:

```text
work-items/<WORK_ITEM_ID>/
```

Review artifacts and summarize reusable learnings.

## Responsibilities

1. Identify useful learnings from this work item.
2. Decide what should be promoted to the knowledge base.
3. Capture user preferences discovered during the work.
4. Capture reusable architecture, testing, security, compliance, and observability patterns.
5. Recommend improvements to the framework itself.
6. When promoting any learning/preference/pattern/ADR, add a matching row to
   `knowledge-base/INDEX.md` in the same step so it stays discoverable.
7. Keep output concise and actionable.

## Output Format

```markdown
## Final Learning Extraction

### Reusable Learnings
- <learning>

### User Preferences Learned
- <preference>

### Reusable Patterns
- <pattern>

### Framework Improvements
- <improvement>

### Knowledge Base Updates Recommended
- <file path> - <reason>

### Do Not Reuse
- <approach that should be avoided>

### Final Summary
<short summary>
```
