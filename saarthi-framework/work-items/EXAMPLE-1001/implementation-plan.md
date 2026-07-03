# Implementation Plan

## Work Item ID
EXAMPLE-1001

## Approach
Backend endpoint + CSV serializer, then UI button. Read-only; no schema changes.

## Tasks
1. Add `CsvSerializer` with RFC-4180 escaping. (unit-tested)
2. Add `OrderService.getOrdersForUser(authUserId)` if not present; ensure
   ordering = most recent first.
3. Add `GET /api/orders/export.csv` controller:
   - resolve user id from session/token only
   - stream CSV; set content-type + attachment filename
   - return 401 when unauthenticated
   - emit audit log (actor, timestamp, row count) and export metric
4. Add "Export CSV" button to Orders page header (disabled while generating).
5. Tests: unit (serializer), integration (auth, ownership scoping, empty history),
   regression run of existing orders suite.

## Files (illustrative)
- `src/export/csvSerializer.*` (new)
- `src/orders/orderService.*` (modify/confirm)
- `src/api/orders/exportController.*` (new)
- `web/orders/OrdersPage.*` (modify)
- tests alongside each.

## Rollout
- Additive, backward-compatible. No migration. Feature flag not required.

## Verification Commands (from work-items/EXAMPLE-1001/verification-commands.yaml)
- build, lint, typecheck, unit_tests, integration_tests, coverage, secret_scan.

## Decision / Assumption Register (proceeded under L2)
| When | Decision / Assumption | Why | Reversible? | Confidence |
|------|-----------------------|-----|-------------|------------|
| design | Stream instead of buffer CSV | avoid timeout on large history | yes | high |
| design | No date filtering in v1 | out of scope per P2 deferral | yes | high |
| design | Light audit (counts only) | balances traceability vs. PII exposure | yes | med |
