# Question Policy

The framework must ask questions only when they improve correctness, product quality, safety, compliance, observability, maintainability, user experience, or delivery confidence.

Questions are not limited to clarification. The framework must also surface best-practice options the user may have missed.

## P0 - Blocking Clarification Questions

Must be answered before proceeding.

Examples:

- Who is allowed to perform this action?
- What happens when validation fails?
- Which system is the source of truth?

## P1 - Recommended Best-Practice Questions

Strongly influence quality, usability, security, compliance, observability, or maintainability.

Examples:

- Should users be notified when this action occurs?
- Should this action be audit logged?
- Should high-risk actions require confirmation or approval?

## P2 - Optional Enhancement Questions

Useful but deferrable.

Examples:

- Should bulk actions be supported?
- Should advanced filtering be added?
- Should scheduled activation be supported?

## Question Budget

- Micro Task: 3
- Small Task: 5
- Standard Feature: 7
- Complex Feature: 12
- High-Risk Enterprise Change: no fixed limit, but prioritize and group
- Prototype: 5

## Consolidation Rules

- Deduplicate questions from all agents.
- Ask one clean question set only.
- Prefer multiple-choice questions when useful.
- Continue clarification loops only for unresolved high-value questions.
- Do not ask questions that are answered by project knowledge, preferences, architecture decisions, or past learnings.
