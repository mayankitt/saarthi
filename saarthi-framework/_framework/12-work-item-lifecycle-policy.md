# Work Item Lifecycle Policy

The framework must treat the work item folder as durable task memory.

## Work Item ID

The user should provide a work item ID whenever possible, such as:

- Jira ticket ID
- Azure DevOps work item ID
- GitHub issue number
- internal task ID
- manually chosen feature ID

## Automatic Folder Mapping

When the user provides a work item ID, automatically use:

```text
work-items/<WORK_ITEM_ID>/
```

If the folder does not exist and file-system write capability exists, create it automatically.

If file-system write capability is unavailable, output exact paths and compact file contents.

## Automatic Artifact Selection

Create only artifacts required by the selected workflow mode.

Do not copy every template for every task.

## One-Time Verification Command Discovery

When a work item is **first initialized**, discover the project's real
verification commands once and cache them in:

```text
work-items/<WORK_ITEM_ID>/verification-commands.yaml
```

This is a one-time activity per work item (chat). On resume, read the cached
file instead of re-discovering. See `framework.config.yaml`
(`verification.discovery`), `_framework/13-execution-verification-loop.md`, and
`templates/verification-commands.yaml`.

## Resume Behavior

When the user references an existing work item ID, automatically attempt to resume from:

```text
work-items/<WORK_ITEM_ID>/work-item-summary.md
```

Then load only relevant phase artifacts.

Do not restart from scratch unless explicitly asked.

## Missing Work Item ID

If no ID is provided, ask once for a work item ID.

If the user wants to proceed without one, generate:

```text
TEMP-YYYYMMDD-short-title
```

Clearly mark it temporary.

## Collision Handling

If the folder exists:

- treat as resume unless user says it is new
- read work-item-summary.md first
- detect conflicting scope
- ask before overwriting or repurposing artifacts
