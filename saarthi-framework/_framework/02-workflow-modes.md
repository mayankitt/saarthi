# Workflow Modes

The **सारथी (Saarthi)** orchestrator must select the lightest safe workflow.

> Source of truth: the machine-readable `workflow_modes`, `budgets`, and
> `definition_of_done` blocks in `framework.config.yaml`. This document explains
> the modes in prose; when the two disagree, the config wins.

## Mode 1: Micro Task

Use for:

- copy/text changes
- small CSS/UI alignment fixes
- simple config updates
- low-risk one-file fixes
- tiny refactors

Default leads:

- **सारथी (Saarthi)**
- Dev Lead
- Code Reviewer if code changes

Question budget: 3

Artifacts:

- requirement-intake.md
- work-item-summary.md

## Mode 2: Small Task

Use for:

- small backend/frontend changes
- minor API changes
- non-critical bug fixes
- small validation changes

Default leads:

- **सारथी (Saarthi)**
- lightweight Design Lead
- Dev Lead
- QA Lead

Conditional leads:

- Security Lead if access, data, or security is touched
- Compliance & Audit Lead if audit-worthy actions are touched

Question budget: 5

Artifacts:

- requirement-intake.md
- clarification-log.md if needed
- implementation-plan.md
- test-plan.md
- work-item-summary.md

## Mode 3: Standard Feature

Use for:

- normal product features
- moderate UI/backend/API work
- feature changes with business rules
- multi-layer application changes

Default leads:

- **सारथी (Saarthi)**
- Product Lead
- Design Lead
- Dev Lead
- QA Lead

Conditional leads:

- Security Lead
- Compliance & Audit Lead
- Observability Lead
- DevOps Lead

Question budget: 7

Artifacts:

- requirement-intake.md
- clarification-log.md
- product-spec.md
- design-spec.md
- implementation-plan.md
- test-plan.md
- work-item-summary.md

## Mode 4: Complex Feature

Use for:

- multi-module features
- cross-system integrations
- significant data model changes
- performance-sensitive flows
- business-critical features

Default leads:

- **सारथी (Saarthi)**
- Product Lead
- Design Lead
- Dev Lead
- QA Lead
- Security Lead
- Observability Lead

Conditional leads:

- Compliance & Audit Lead
- DevOps Lead

Question budget: 12

Artifacts:

- all Standard Feature artifacts
- security-review.md if security-relevant
- observability-plan.md
- devops-release-plan.md if deployment risk exists
- audit-compliance-review.md if audit/compliance-relevant

## Mode 5: High-Risk Enterprise Change

Use for:

- authentication
- authorization
- role/permission changes
- admin actions
- personal/sensitive data
- payment/order/booking/customer-impacting flows
- audit/compliance-heavy operations
- production stability risk

Default leads:

- **सारथी (Saarthi)**
- Product Lead
- Design Lead
- Security Lead
- Compliance & Audit Lead
- Observability Lead
- Dev Lead
- QA Lead
- DevOps Lead if release/deployment risk exists

Question budget: no fixed limit, but prioritized and grouped.

Mandatory artifacts:

- requirement-intake.md
- clarification-log.md
- product-spec.md
- design-spec.md
- implementation-plan.md
- test-plan.md
- security-review.md
- audit-compliance-review.md
- observability-plan.md
- work-item-summary.md

Conditional artifact:

- devops-release-plan.md

## Mode 6: Prototype / Exploration

Use only when explicitly requested.

Assumptions are allowed but must be documented.

Question budget: 5 unless critical safety/security ambiguity exists.
