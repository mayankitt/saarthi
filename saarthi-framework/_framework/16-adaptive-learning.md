# Adaptive Learning & Self-Evolution Policy

The framework evolves alongside the user. Over time, Saarthi learns your
engineering patterns, preferences, and priorities so you need to repeat them
less and less. The ultimate goal is to become a **software engineering twin**
of the user — capable of taking on tasks with fewer interruptions, while
staying aligned to core safety and quality principles.

Source of truth for thresholds: the `adaptive_learning` block in
`framework.config.yaml`.

---

## 1. What to Learn

Saarthi actively observes and records:

| Category | Examples |
|---|---|
| **Coding style** | preferred language idioms, formatting, naming conventions |
| **Workflow preferences** | preferred autonomy level, question verbosity, artifact depth |
| **Technology choices** | favored libraries, test frameworks, cloud providers |
| **Decision patterns** | how you resolved past trade-offs (security vs speed, sync vs async) |
| **Review sensitivities** | areas you always want to review vs areas you delegate fully |
| **Communication style** | terse or detailed responses, preferred summary format |
| **Risk tolerance** | which change types you approve instantly vs require confirmation |

---

## 2. When to Capture Preferences

Capture a preference **proactively** at the end of any interaction where the
user explicitly corrects, overrides, or selects one approach over another. Also
capture implicitly when a strong pattern emerges across ≥ 2 work items.

### Explicit triggers (capture immediately)
- User corrects the agent's choice ("use `async/await`, not callbacks")
- User rejects a default and picks an alternative
- User states a blanket rule ("always add error boundaries")
- User answers a P1/P2 question consistently across work items

### Implicit triggers (capture after pattern confirmation)
- Same technology/pattern chosen in 2+ consecutive work items
- Same autonomy override applied in 3+ interactions
- Same formatting or architecture decision applied without being asked

---

## 3. Confidence & Criticality Model

Before applying a learned preference without asking, evaluate:

| Dimension | Low | Medium | High |
|---|---|---|---|
| **Confidence** | first observation | 2 consistent signals | 3+ consistent signals |
| **Criticality** | cosmetic/style | implementation details | security/auth/data/infra |
| **Reversibility** | trivially undoable | needs rework | irreversible |

### Application rules

| Confidence | Criticality | Reversibility | Action |
|---|---|---|---|
| High | Low | High | Apply silently; note in decision register |
| High | Low | Low | Apply silently; note in decision register |
| High | Medium | High | Apply with brief note ("used your preference: X") |
| High | Medium | Low | Apply with brief note; offer override |
| Any | High | Any | **Always ask** — no preference overrides a high-criticality decision |
| Medium | Low | High | Apply with brief note |
| Medium | Medium | Any | Ask once with preference pre-selected as default |
| Low | Any | Any | Ask with no pre-selection |

**Critical principle**: The threshold to skip user confirmation scales
proportionally with criticality and predictability. Style choices can be
applied silently at high confidence. Security, authentication, data schema, or
infrastructure decisions always require explicit confirmation, regardless of
how many times a preference has been observed.

---

## 4. Persistence Format

Preferences are stored in `knowledge-base/preferences/`. See
`knowledge-base/preferences/README.md` for the canonical file format.

Each preference record has:
- `id` — unique slug
- `category` — one of: `workflow`, `coding-style`, `technology`, `decision-pattern`, `review`, `communication`, `risk-tolerance`
- `statement` — the preference in plain English
- `confidence` — `low` | `medium` | `high`
- `criticality` — `low` | `medium` | `high`
- `source` — `explicit` | `implicit`
- `observed_count` — number of times reinforced
- `last_seen` — ISO date of last reinforcement
- `examples` — 1–3 short concrete examples (work item IDs or descriptions)

---

## 5. Preference Application During Tasks

At the start of each new work item (intake phase):

1. Load `knowledge-base/INDEX.md`.
2. Filter `preferences/` entries relevant to the current task type, language,
   and technology stack.
3. Apply high-confidence, low-criticality preferences silently.
4. Surface medium-confidence or medium-criticality preferences as P2 defaults
   (pre-selected, easy to override).
5. Never auto-apply high-criticality preferences — always confirm.

---

## 6. Preference Learning During Finalization

At the finalize phase (`10-finalize-work-item-prompt.md`), extract new
preferences using this checklist:

- [ ] Did the user override any framework default? → candidate preference
- [ ] Did the user consistently choose the same pattern across phases? → candidate
- [ ] Did the user ask for a style that was not the default? → candidate
- [ ] Did the user answer a P1/P2 question the same way as a prior work item? → promote confidence

For each candidate:
1. Check if an existing preference entry in the KB already covers it.
2. If yes, increment `observed_count` and update `last_seen`.
3. If no, create a new entry with `confidence: low` (first observation).
4. Add or update the index row in `knowledge-base/INDEX.md`.

---

## 7. Preference Decay & Contradiction Handling

- If the user overrides a `high`-confidence preference, **downgrade** it to
  `medium` and flag it as `contradicted`.
- If overridden a second time in the same direction, update the preference to
  the new value and reset confidence to `medium`.
- Preferences that have not been seen in 90+ days should be flagged for review
  at the next relevant task (ask once: "Still prefer X?").

---

## 8. Framework Self-Improvement

Beyond user preferences, the framework improves itself. After each finalized
work item, check:

- Did a quality gate catch a real issue? → reinforce the gate
- Did a template lack a key field? → propose adding it
- Did a policy cause confusion or workarounds? → flag for improvement
- Did a new tool or pattern prove superior? → add to `reusable-patterns/`

Framework improvement candidates are recorded in the `Framework Improvements`
section of the Final Learning Extraction template
(`templates/final-learning-extraction.md`) and reviewed periodically.
