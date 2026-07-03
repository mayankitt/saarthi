# Clarification Log

## Work Item ID
EXAMPLE-1001

## Question Round 1

### P0 - Blocking
| # | Question | Answer |
|---|----------|--------|
| 1 | Should export be limited to the user's own orders only (no admin/bulk)? | Yes, own orders only for this work item. |
| 2 | Which columns must the CSV include? | order_id, order_date, status, item_count, total_amount, currency. |

### P1 - Recommended Best Practice
| # | Question | Answer |
|---|----------|--------|
| 3 | Should the export action be audit-logged? | Light audit: log actor + timestamp + row count, no order contents. |
| 4 | Should large histories be streamed to avoid timeouts? | Yes, stream/page the response. |

### P2 - Optional Enhancement
| # | Question | Answer |
|---|----------|--------|
| 5 | Add date-range filtering? | Deferred to a future work item. |

## Resolved Assumptions
- CSV uses UTF-8 with a header row and RFC-4180 escaping.
- order_date is ISO-8601; total_amount is decimal with currency code.
