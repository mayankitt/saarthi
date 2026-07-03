# Model Selection Policy

Use the lightest suitable model tier while preserving quality, safety, and traceability.

This policy is vendor-agnostic. Map tiers to the available models in your environment.

> Source of truth for the tier -> concrete model mapping and per-mode default
> tiers is `models.tier_map` and `workflow_modes.*.model_tier` in
> `framework.config.yaml`. Set the real model names there once per environment.

## Tier 1: Light Model

Use for small text edits, simple refactors, formatting, renaming, low-risk boilerplate, simple unit tests, and small UI tweaks.

## Tier 2: Standard Model

Use for normal feature implementation, moderate bug fixes, localized backend/frontend changes, test generation, API/client updates, small database changes, and standard code review.

## Tier 3: Heavy Reasoning Model

Use for architecture design, complex business rules, ambiguous requirements, cross-system design, performance-sensitive work, security-sensitive work, compliance-sensitive work, complex debugging, and concurrency/distributed-system concerns.

## Tier 4: Specialist / Deep Review Model

Use sparingly for final architecture review, security threat review, compliance/audit validation, production incident root cause analysis, high-risk release review, and critical performance diagnosis.

## Rules

- Use the cheapest model that can safely do the job.
- Escalate only with justification.
- De-escalate when the task becomes simpler.
- Prefer phase-aware model usage: heavier for design/review, lighter for repetitive implementation where safe.

## Output Requirement

Always include:

```text
Model Strategy:
- Selected Tier:
- Reason:
- Escalation Triggers:
- De-escalation Opportunity:
```
