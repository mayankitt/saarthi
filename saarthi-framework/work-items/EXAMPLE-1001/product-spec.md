# Product Spec

## Work Item ID
EXAMPLE-1001

## Summary
Self-service CSV export of a signed-in user's own order history from the Orders
page.

## User Story
As a signed-in customer, I want to download my order history as a CSV so that I
can keep an offline record and track expenses.

## Business Rules
- A user may export only their own orders.
- Export reflects the same orders visible on the user's Orders page.
- Ordering: most recent order first.

## Acceptance Criteria
See `requirement-intake.md` AC1-AC6 (single source; not duplicated here).

## MVP Slice
- Single "Export CSV" button -> full history of the current user, fixed columns.

## Non-Goals
- Admin/bulk export, alternate formats, scheduling, filtering.

## UX Notes
- Button on Orders page header; disabled state while generating.
- Filename: `orders-<yyyymmdd>.csv`.
- Empty history still downloads a valid header-only file (no error).
