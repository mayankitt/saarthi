# Quality Gates

Apply gates based on workflow mode and risk.

## Evidence Requirement (applies to all gates)

When `verification.evidence_required` is true in `framework.config.yaml`
(default), a gate passes only with **objective evidence**, not self-report.
For any check that runs a command (build, lint, typecheck, tests, coverage,
secret scan), paste the actual command output. See
`13-execution-verification-loop.md`. Record evidence in
`work-item-summary.md`.

The binding pass/fail criteria are the `definition_of_done` profiles in
`framework.config.yaml`. The current workflow mode selects the profile.

## Requirement Readiness Gate

Relevant items must be clear:

- user/persona
- problem
- expected outcome
- in scope
- out of scope
- acceptance criteria
- failure and edge cases
- security considerations
- performance expectations
- data created/read/updated/deleted
- testing needs
- existing system constraints

Not every item applies to every task. The Master and Design Lead decide relevance.

## Design Readiness Gate

Before development:

- architecture approach is clear
- data model changes are identified
- API/interface changes are identified
- test strategy is defined
- security risks are addressed if relevant
- compliance/audit requirements are defined if relevant
- observability requirements are defined if relevant
- deployment/rollback concerns are identified if relevant

## Development Quality Gate

Before QA:

- implementation follows project conventions
- code is cohesive and minimal
- edge cases are handled
- meaningful tests are added
- no unrelated refactoring is introduced
- error handling is appropriate
- performance considerations are addressed
- build, lint, and typecheck pass **with pasted evidence**
- new tests pass **with pasted evidence**

## Self-Review Gate

Before declaring done (Standard profile and above), perform an explicit
self-review acting as Architecture Critic + Code Reviewer, and record the
outcome:

- change matches the agreed design and scope (no scope creep)
- naming, structure, and error handling are sound
- no dead code, debug logging, secrets, or commented-out blocks
- public interfaces and side effects are intentional
- a reviewer could understand the change without verbal explanation

Output a short self-review note (pass / pass-with-notes / fail). A failing
self-review blocks done.

## Regression Gate

Before QA/release:

- the **existing** test suite runs and is green (not only new tests)
- evidence pasted
- any newly-failing existing test is fixed at the cause, never deleted or
  skipped to force green

## Security Gate

Required for sensitive or privileged changes:

- backend/system-boundary authorization checks exist
- input validation is appropriate
- sensitive data is protected
- abuse prevention is considered
- security tests exist
- a secret scan runs and is clean (no committed secrets/credentials);
  evidence pasted where a scan command is configured

## Compliance & Audit Gate

Required for audit-relevant changes:

- audit-worthy actions are identified
- audit event schemas are defined
- sensitive data is not over-logged
- actor, target, timestamp, outcome, request ID, and correlation ID are captured where relevant
- audit behavior is tested
- retention/access considerations are documented

## Observability Gate

Required for production-relevant features:

- logs are meaningful and safe
- metrics are identified
- correlation/trace IDs are propagated where applicable
- alerts are defined for critical failures
- post-release validation is clear

## Release Gate

Before release:

- all Definition-of-Done fields for the mode's profile are satisfied **with evidence**
- validator passes: `node tools/validate-work-item.js <WORK_ITEM_ID>`
- tests pass (new + regression) with pasted evidence
- self-review gate passed
- reviews are complete
- rollback approach is documented if relevant
- observability is ready
- security/compliance gates are passed if applicable
- secret scan is clean if applicable
- known risks are accepted or resolved
