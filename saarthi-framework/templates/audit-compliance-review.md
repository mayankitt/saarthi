# Audit & Compliance Review

## Work Item ID
<id>

## Compliance Relevance
Low / Medium / High

## Why This Is Audit-Relevant
<brief reason>

## Audit-Worthy Events
1. Event Name:
   - Trigger:
   - Actor:
   - Target:
   - Outcome:
   - Required: Yes / No

## Audit Event Schema

```json
{
  "eventType": "<EVENT_NAME>",
  "actor": {
    "userId": "<id>",
    "role": "<role>"
  },
  "target": {
    "entityType": "<entity>",
    "entityId": "<id>"
  },
  "change": {
    "field": "<field>",
    "before": "<previous value>",
    "after": "<new value>"
  },
  "context": {
    "requestId": "<request id>",
    "correlationId": "<correlation id>",
    "sourceIp": "<ip if applicable>",
    "channel": "<channel>"
  },
  "outcome": "SUCCESS_OR_FAILURE",
  "timestamp": "<timestamp>"
}
```

## Sensitive Data Handling
- Do not log:
  - <field>
- Mask:
  - <field>
- Hash/tokenize:
  - <field>

## Retention Considerations
- Required retention:
- Unknown / needs policy confirmation:

## Access Control for Audit Logs
- Who can view:
- Who can export:
- Who can delete:
- Tamper resistance needed: Yes / No

## Traceability Matrix

| Requirement | Design Decision | Code Area | Test Case | Audit Event |
|---|---|---|---|---|
| <req> | <decision> | <path> | <test> | <event> |

## Compliance Questions
- <question>

## Required Tests
- Audit event emitted on success.
- Audit event emitted on failure where relevant.
- Sensitive data is not logged.
- Actor and target are correctly captured.
- Correlation ID is present.

## Compliance Recommendation
Approved / Approved with Conditions / Blocked
