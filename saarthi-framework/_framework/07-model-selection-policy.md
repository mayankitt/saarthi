# Model Selection Policy

Use the lightest suitable model tier while preserving quality, safety, and traceability.

This policy is vendor-agnostic. Map tiers to the available models in your environment.

> Source of truth for the tier → concrete model mapping and per-mode default
> tiers is `models.tier_map`, `models.capability_aliases`, and
> `workflow_modes.*.model_tier` in `framework.config.yaml`.
> Set the real model names there once per environment.

## Capability Aliases

Capability aliases are the **preferred human-readable names** to use in prompts,
policies, and agent instructions. The orchestrator resolves each alias to the
underlying tier key, then looks up the configured model.

| Alias | Tier key | Use for |
|---|---|---|
| `fast` | `tier_1_light` | Small edits, formatting, renaming, low-risk boilerplate, simple unit tests |
| `standard` | `tier_2_standard` | Normal feature work, bug fixes, test generation, API/client updates, code review |
| `reasoning` | `tier_3_heavy` | Architecture, complex debugging, cross-system design, security/compliance work |
| `expert` | `tier_4_specialist` | Final review, security threat model, compliance audit, production incident RCA |

Use aliases in prose ("use the **reasoning** model for architecture decisions") and
tier keys only when writing or reading `framework.config.yaml` directly.

## Tier 1 — `fast` (Light Model)

Small text edits, simple refactors, formatting, renaming, low-risk boilerplate, simple unit tests, and small UI tweaks.

## Tier 2 — `standard` (Standard Model)

Normal feature implementation, moderate bug fixes, localized backend/frontend changes, test generation, API/client updates, small database changes, and standard code review.

## Tier 3 — `reasoning` (Heavy Reasoning Model)

Architecture design, complex business rules, ambiguous requirements, cross-system design, performance-sensitive work, security-sensitive work, compliance-sensitive work, complex debugging, and concurrency/distributed-system concerns.

## Tier 4 — `expert` (Specialist / Deep Review Model)

Use sparingly for final architecture review, security threat review, compliance/audit validation, production incident root cause analysis, high-risk release review, and critical performance diagnosis.

## Rules

- Use the cheapest model (or alias) that can safely do the job.
- Escalate only with justification.
- De-escalate when the task becomes simpler.
- Prefer phase-aware model usage: heavier for design/review, lighter for repetitive implementation where safe.
- Reference aliases in prose; use tier keys only in config.

## Output Requirement

Always include:

```text
Model Strategy:
- Selected Alias / Tier:
- Reason:
- Escalation Triggers:
- De-escalation Opportunity:
```
