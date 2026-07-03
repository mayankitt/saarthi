# Token Optimization Policy

The framework must minimize unnecessary token usage while preserving quality, safety, and traceability.

## Core Rules

1. Be concise by default.
2. Do not repeat full context unless needed.
3. Prefer summaries over full artifact dumps.
4. Use references to existing artifacts instead of copying full contents.
5. Ask only high-value questions.
6. Avoid generic best-practice lectures.
7. Avoid reprinting unchanged sections.
8. Update only changed artifact sections.
9. Use checklists where possible.
10. Keep `work-item-summary.md` current.

## Response Size Modes

### Compact

Use for normal daily interaction.

Output only classification, key questions, next step, and changed artifacts.

### Standard

Use for feature planning/design.

Output moderate detail, important reasoning, and key decisions.

### Detailed

Use only for deep analysis, high-risk enterprise changes, architecture/security/compliance review, or final design review.

## Context Loading Order

1. `work-item-summary.md`
2. current phase artifact
3. relevant decisions
4. relevant reusable patterns
5. relevant preferences

Do not load all artifacts unless resuming after long inactivity, resolving conflict, or performing final review.

## Artifact Update Rules

- Show only changed sections.
- Do not rewrite full artifacts unless asked.
- Mention impacted files.
- Keep changelog brief.

## Question Optimization

Before asking a question, check:

- Is the answer required now?
- Can it be deferred?
- Can it be inferred from documented preferences?
- Is it relevant to the selected workflow mode?
- Is it worth the token cost?

If not, do not ask it.
