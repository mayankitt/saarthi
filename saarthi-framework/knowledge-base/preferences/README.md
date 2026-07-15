# Preferences

Store stable user/project preferences so agents ask fewer repeated questions over time.

## File naming

Use `<category>-<slug>.md` — for example `coding-style-typescript.md`,
`workflow-autonomy.md`, `technology-testing-framework.md`.

## Preference record format

```markdown
---
id: <unique-slug>
category: workflow | coding-style | technology | decision-pattern | review | communication | risk-tolerance
confidence: low | medium | high
criticality: low | medium | high
source: explicit | implicit
observed_count: <integer>
last_seen: <YYYY-MM-DD>
---

# <Short preference title>

**Statement:** <The preference in one plain-English sentence.>

**Examples:**
- <Work item ID or brief description where this was observed>
- <Another example>

**Application rule:** <When and how to apply this preference automatically.>

**Override signal:** <What user input would indicate this preference no longer applies.>
```

## Application rules (summary)

| Confidence | Criticality | Apply without asking? |
|---|---|---|
| high | low | Yes — silent, note in decision register |
| high | medium | Yes — brief note to user, offer override |
| high | high | **No** — always ask |
| medium | low | Yes — brief note to user |
| medium | medium | Ask once, pre-select as default |
| low | any | Ask, no pre-selection |

See `_framework/16-adaptive-learning.md` for the full policy.
