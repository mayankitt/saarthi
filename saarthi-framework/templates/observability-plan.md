# Observability Plan

## Work Item ID
<id>

## Observability Relevance
Low / Medium / High

## Key User/System Journeys To Observe
- <journey>

## Logs

### Required Log Events
- <event>

### Fields To Include
- requestId
- correlationId
- userId if safe
- operation
- outcome
- duration
- errorCode

### Fields To Avoid
- passwords
- tokens
- secrets
- sensitive personal data
- full payment details

## Metrics
- Success count:
- Failure count:
- Latency:
- Throughput:
- Retry count:
- Validation failures:
- Authorization failures:

## Traces
- Trace boundaries:
- External calls:
- Database calls:

## Alerts
- Alert:
  - Condition:
  - Severity:
  - Owner:

## Dashboards
- Required: Yes / No
- Suggested panels:
  - <panel>

## Observability Tests
- Logs emitted correctly.
- Correlation ID propagated.
- Metrics updated.
- Errors are observable.

## Open Questions
- <question>
