# Minimum Viable Ceremony Rule

Use the lightest workflow that still protects:

- correctness
- maintainability
- security
- compliance
- observability
- testability
- user experience

Do not invoke unnecessary agents.

Do not create heavy artifacts for trivial tasks.

If a feature touches privileged actions, sensitive data, authentication, authorization, audit-worthy workflows, customer-impacting flows, or production stability, increase ceremony appropriately.

If unsure whether a task is low-risk or high-risk, ask one concise clarification question.
