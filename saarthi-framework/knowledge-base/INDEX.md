# Knowledge Base Index

Read this file **first** when you need prior knowledge. It lets you load only the
relevant entries instead of reading the entire knowledge base (token discipline).

As the knowledge base grows, keep this index current: one row per entry with
enough tags for an agent to decide relevance without opening the file.

## How to use

1. Read this index.
2. Match the current task's tags/keywords against the `Tags` column.
3. Open only the matching entries (preferences, patterns, ADRs, learnings).
4. If nothing matches, proceed without loading the KB.

## Preferences

| File | Tags | Summary |
|------|------|---------|
| `preferences/README.md` | meta | How to record stable user/project preferences. |

## Reusable Patterns

| File | Tags | Summary |
|------|------|---------|
| `reusable-patterns/README.md` | meta | How to record reusable implementation/test/security patterns. |

## Architecture Decisions (ADRs)

| File | Tags | Status | Summary |
|------|------|--------|---------|
| `architecture-decisions/ADR-template.md` | meta, template | n/a | Template for new ADRs. |

## Engineering Standards

| File | Tags | Summary |
|------|------|---------|
| `engineering-standards/README.md` | meta | How to record engineering standards. |

## Past Learnings

| File | Tags | Summary |
|------|------|---------|
| `past-learnings/README.md` | meta | How to record reusable learnings from finalized work items. |

---

When the Finalize flow (`_framework/10-finalize-work-item-prompt.md`) promotes a
learning, preference, pattern, or ADR, **add a row here in the same step**. An
entry that is not indexed will not be found efficiently.
