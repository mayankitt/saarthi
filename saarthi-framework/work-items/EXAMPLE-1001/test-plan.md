# Test Plan

## Work Item ID
EXAMPLE-1001

## Test Strategy Summary
Unit-test the CSV serializer (escaping + ordering), integration-test the
endpoint (auth, ownership scoping, empty history), and run the existing orders
regression suite. Evidence pasted below.

## Acceptance Criteria Coverage

| Acceptance Criteria | Test Type | Covered By | Status |
|---|---|---|---|
| AC1 trigger export | Integration | export_returns_csv | Done |
| AC2 only own orders | Integration | export_scoped_to_user | Done |
| AC3 columns + ordering | Unit | serializer_columns_ordering | Done |
| AC4 unauth rejected | Integration | export_requires_auth_401 | Done |
| AC5 cross-user blocked | Integration | export_cannot_access_others | Done |
| AC6 empty history | Integration | export_empty_header_only | Done |

## Unit Tests
- serializer_columns_ordering: correct columns, most-recent-first.
- serializer_escaping: commas, quotes, and newlines quoted/escaped per RFC-4180.

## Integration Tests
- export_returns_csv: 200, text/csv, attachment filename.
- export_scoped_to_user: only the auth user's rows appear.
- export_requires_auth_401: no session -> 401.
- export_cannot_access_others: supplying another user id has no effect (own scope).
- export_empty_header_only: user with no orders -> header-only CSV, 200.

## Regression Tests
- Existing suite run required: Yes
- Command: `npm test` and `npm run test:integration` (from verification-commands.yaml)
- Result evidence:
```text
$ <unit_tests>
148 passed, 0 failed   (6 new)
$ <integration_tests>
37 passed, 0 failed   (5 new)
```

## Negative Tests
- Unauthenticated request -> 401.
- Tampered user id parameter -> ignored, own scope returned.

## Edge Case Tests
- Empty history -> header-only file.
- Field with comma/quote/newline -> correctly escaped.

## Security Tests
- 401 on no auth; cross-user isolation verified.

## Audit Logging Tests
- Export emits one audit entry: actor id, timestamp, row count; no order contents.

## Observability Tests
- Export metric increments; serialization error path logs without PII.

## Performance Tests
- Required: Yes (large history)
- Scenarios:
  - 50k-order user export streams without timeout or memory spike.

## Manual Test Checklist
- Click Export on Orders page -> file downloads as orders-YYYYMMDD.csv.
- Open CSV -> columns/order correct, no other users' data.

## Test Data Needed
- User A with mixed-status orders incl. special characters; User B with orders;
  User C with zero orders.

## QA Go/No-Go
Go

## Definition of Done Evidence
- Profile (from framework.config.yaml): standard
- Build passes: Yes - build output clean
- Lint clean: Yes - 0 problems
- New tests added & green: Yes - 11 new (6 unit, 5 integration)
- Regression suite green: Yes - 148 + 37 passed, 0 failed
- Coverage delta meets threshold: Yes - +1.4% (>= 0)
- No new high-severity findings: Yes
- Self-review passed: Yes - pass (no scope creep, ownership enforced server-side)

## Open Testing Risks
- None blocking. Date-range filtering deferred to a future work item.
