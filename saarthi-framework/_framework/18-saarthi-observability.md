# Saarthi Observability & Debug Log

Saarthi emits a **lightweight, per-work-item debug log** that records its own
orchestration decisions — not the target application's observability. This makes
it easy to review *why* the framework made a particular classification, which
preference it applied, or when a budget alarm fired.

The log is **append-only, human-readable, and opt-in** (controlled via
`saarthi_observability.enabled` in `framework.config.yaml`).

---

## Log location

```text
work-items/<WORK_ITEM_ID>/saarthi-debug.log.md
```

The log is a Markdown file so it renders naturally in any editor.

---

## Log entry format

Every event is one fenced block:

````text
```saarthi-log
event: <EVENT_NAME>
work_item_id: <ID>
timestamp: <YYYY-MM-DDTHH:MM:SSZ>
[additional key-value pairs specific to the event]
```
````

Rules:
- Always append; never overwrite or truncate.
- Include `event`, `work_item_id`, and `timestamp` in every entry.
- Redact any value that looks like a secret, token, or credential — write
  `"[REDACTED]"` instead (governed by `saarthi_observability.redact_sensitive_values`).
- Keep entries concise; prefer one sentence for `notes`.

---

## Canonical event names

| Event | When to emit | Key extra fields |
|---|---|---|
| `intake_started` | Work item intake begins | `raw_requirement_words` (word count, not full text) |
| `mode_classified` | Workflow mode chosen | `mode`, `risk`, `reason` |
| `probe_result` | Capability probe evaluated | `normalized_score`, `recommended_level` |
| `kb_hit` | Knowledge-base entry loaded | `entry_path`, `matched_tags` |
| `preference_applied` | Adaptive preference applied silently | `preference_id`, `confidence`, `criticality` |
| `budget_alarm` | Token estimate crossed `stop_and_report_at` | `mode`, `estimated_tokens`, `threshold` |
| `gate_result` | Quality gate evaluated | `gate`, `phase`, `status` (`green`/`red`/`skipped`) |
| `tool_invoked` | MCP tool or agent capability used | `tool`, `reason` |
| `orchestration_downgrade` | Orchestration level downgraded mid-task | `from_level`, `to_level`, `reason` |
| `work_item_closed` | Work item finalized and validated | `dod_profile`, `validation_status` |

---

## Example log excerpt

````markdown
```saarthi-log
event: intake_started
work_item_id: JIRA-1234
timestamp: 2026-07-27T09:00:00Z
raw_requirement_words: 47
```

```saarthi-log
event: mode_classified
work_item_id: JIRA-1234
timestamp: 2026-07-27T09:00:03Z
mode: standard_feature
risk: medium
reason: "multi-endpoint API change with DB migration; no auth/security changes detected"
```

```saarthi-log
event: kb_hit
work_item_id: JIRA-1234
timestamp: 2026-07-27T09:00:05Z
entry_path: preferences/coding-style-typescript.md
matched_tags: typescript, coding-style
```

```saarthi-log
event: preference_applied
work_item_id: JIRA-1234
timestamp: 2026-07-27T09:00:06Z
preference_id: coding-style-typescript
confidence: high
criticality: low
notes: "applied silently; prefer const over let"
```

```saarthi-log
event: gate_result
work_item_id: JIRA-1234
timestamp: 2026-07-27T09:45:00Z
gate: dod_standard
phase: release
status: green
```

```saarthi-log
event: work_item_closed
work_item_id: JIRA-1234
timestamp: 2026-07-27T09:46:00Z
dod_profile: standard
validation_status: passed
```
````

---

## When to emit log entries

The framework emits log entries automatically at the following phase boundaries:

- **Intake**: `intake_started`, then `mode_classified` after classification
- **Capability probe** (if run): `probe_result`
- **KB lookup** (if `require_index_lookup_at_intake: true`): `kb_hit` per matched entry
- **Adaptive learning**: `preference_applied` for each silently applied preference
- **Budget check**: `budget_alarm` when estimate crosses `stop_and_report_at`
- **Quality gates**: `gate_result` at each phase boundary (design / dev / release)
- **Tool use**: `tool_invoked` for each MCP server or external tool call
- **Orchestration downgrade**: `orchestration_downgrade` if capability signals degrade
- **Finalize**: `work_item_closed` after `validate_work_item.py` passes

Do not emit log entries for routine internal reasoning steps — only emit at
observable decision points.

---

## Privacy & sensitivity rules

1. Never log the full requirement text — log only `raw_requirement_words` (word count).
2. Never log file contents, diffs, or code snippets.
3. Never log authentication tokens, credentials, or environment variables.
4. If `saarthi_observability.redact_sensitive_values: true` (the default), any
   field value matching a secret pattern must be replaced with `"[REDACTED]"`.
5. The log file is part of the work-item folder; apply the same access controls
   as the rest of the work-item artifacts.

---

## Configuration reference

All settings live in `framework.config.yaml` under the `saarthi_observability` block:

```yaml
saarthi_observability:
  enabled: true                     # Master switch; set false to suppress all log output
  log_file: "saarthi-debug.log.md"  # Path relative to work-items/<ID>/
  log_events:                       # List of event names to emit; omit = all events
    - intake_started
    - mode_classified
    - probe_result
    - kb_hit
    - preference_applied
    - budget_alarm
    - gate_result
    - tool_invoked
    - orchestration_downgrade
    - work_item_closed
  include_timestamps: true
  redact_sensitive_values: true     # Never log secrets or tokens
```

To disable the log entirely, set `enabled: false`.
To capture only a subset of events, list only the desired event names in `log_events`.
