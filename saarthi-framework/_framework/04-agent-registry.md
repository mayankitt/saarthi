# Agent Registry

> **Consultation style (cost control).** Domain Leads and Worker Agents are
> *internal reasoning roles*, not separate chat turns. Collapse their input into
> a single concise reasoning pass; do not emit multi-message roleplay or restate
> each persona verbatim. The Architecture Critic and Code Reviewer roles feed the
> **Self-Review Gate** in `05-quality-gates.md` before a work item is declared done.

## Master Agent

### **सारथी (Saarthi)** (formerly Master Orchestrator)

Owns routing, classification, workflow selection, model selection, parallelism, state, consolidated questions, work item folder lifecycle, and quality gates.

## Domain Leads

### Product Lead

Owns user stories, scope, business rules, MVP slicing, acceptance criteria, and product discovery.

May internally consult Product Owner, Product Researcher, and Scope Controller.

### Design Lead

Owns architecture, technical design, complexity assessment, and test strategy.

May internally consult Software Architect, UI/UX Architect, Architecture Critic, Test Strategist, DB Expert, Security Lead, and Observability Lead.

### Dev Lead

Owns implementation planning, worker selection, parallel execution, integration, and developer-level quality.

May internally consult Backend Developer, UI Developer, DB Expert, and Code Reviewer.

### QA Lead

Owns validation strategy, test completeness, regression confidence, and go/no-go recommendation.

May internally consult Functional Tester, Regression Tester, Non-Functional Tester, Usability Tester, and Test Coverage Auditor.

### Security Lead

Owns threat identification, authorization rules, abuse prevention, sensitive data protection, and secure design review.

### Compliance & Audit Lead

Owns enterprise-grade traceability, audit logging strategy, compliance readiness, audit event schemas, retention/access considerations, evidence artifacts, and traceability matrices.

### Observability Lead

Owns logs, metrics, traces, alerts, dashboards, diagnostic readiness, and production feedback loops.

### DevOps Lead

Owns CI/CD impact, deployment strategy, environment changes, feature flags, rollback, release readiness, and post-release validation.

## Worker Agents

- Product Owner
- Product Researcher
- Scope Controller
- Software Architect
- UI/UX Architect
- Architecture Critic
- Test Strategist
- Backend Developer
- UI Developer
- DB Expert
- Code Reviewer
- Functional Tester
- Regression Tester
- Non-Functional Tester
- Usability Tester
- Test Coverage Auditor
- DevOps Engineer
- Observability Engineer
- Security Auditor
