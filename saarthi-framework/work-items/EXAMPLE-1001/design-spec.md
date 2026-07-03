# Design Spec

## Work Item ID
EXAMPLE-1001

## Architecture Approach
Add a read-only export endpoint and a UI action. Reuse the existing orders query
layer; add a CSV serializer. No schema changes.

```text
[Orders Page] --click Export--> GET /api/orders/export.csv (auth required)
        -> OrderService.getOrdersForUser(authUserId)   # ownership from session, not request
        -> CsvSerializer.stream(orders)                # RFC-4180 escaping, streamed
        -> 200 text/csv  (Content-Disposition: attachment; filename="orders-YYYYMMDD.csv")
```

## Key Design Decisions
- **Authorization source of truth:** the authenticated user id comes from the
  session/token, never from a client-supplied parameter. (Mitigates AC5.)
- **Streaming:** stream rows to avoid timeouts/memory spikes on large histories.
- **No new persistence:** pure read + serialize.

## Data Model
- No changes. Reads existing `orders` for the authenticated user.

## API / Interface Changes
- New: `GET /api/orders/export.csv`
  - Auth: required (401 if missing).
  - Returns: `text/csv`, header row + one row per order, most recent first.
  - Errors: 401 unauthenticated; 500 on serialization failure (logged, no PII).

## CSV Contract
```text
order_id,order_date,status,item_count,total_amount,currency
1042,2026-06-21T10:03:00Z,SHIPPED,3,129.97,USD
```
Escaping: fields containing `,` `"` or newlines are quoted; embedded `"` doubled.

## Test Strategy
Unit (serializer escaping + ordering), integration (endpoint auth + ownership
scoping + empty history), regression (existing orders suite). See `test-plan.md`.

## Security / Audit / Observability
- Security: ownership enforced server-side; security tests for 401 and cross-user 403/empty.
- Audit (light): log actor id, timestamp, row count on export. No order contents logged.
- Observability: count + latency metric for exports; error log on serialization failure.
