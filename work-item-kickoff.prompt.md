---
mode: ask
description: "Start a new work item with the सारथी (Saarthi) agent: classify mode/risk, ask grouped P0-P2 questions, and output the initial execution plan."
---

Use this kickoff template to start a work item.

Work Item ID (optional): <e.g. ABC-1234>
Requirement: <plain-English requirement>
Business goal: <why this matters>
Constraints: <deadlines, tech, compliance, security, performance>
Autonomy preference: <L1 ask-often / L2 act-and-checkpoint / L3 act-and-report>

If Work Item ID is omitted, auto-generate a readable ID in the format:
`WI-YYYYMMDD-short-title`.

Then do the following:
1. Classify type, risk, scope, and the lightest safe workflow mode.
2. Ask one grouped question set only: P0, P1, P2.
3. Propose the smallest safe implementation slice.
4. Define verification approach and what evidence will be required for done.
5. List artifacts to create/update for this mode.
