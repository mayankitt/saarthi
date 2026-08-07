# सारथी (Saarthi) — Multi-Agent Orchestration Framework

> [!NOTE]
> **सारथी (Saarthi)** is a Sanskrit word meaning *charioteer* or *guide*. True to its name, this framework guides your AI agents through the software development lifecycle with strict control, safety guardrails, and quality gates.

**सारथी (Saarthi)** is an elegant, lightweight, and agent-agnostic software engineering operating model designed to maximize developer productivity. It provides a structured environment for AI coding assistants (like GitHub Copilot, Claude Code, or editor agents) to operate in, ensuring high-quality software delivery through automated verification and multi-agent coordination.

---

## Key Features

- 🤖 **Structured AI Agent Guidance**: Binds to your AI coding assistant to enforce strict rules, preventing agents from guessing requirements or adding unsanctioned code.
- ⚙️ **Machine-Readable Control Plane**: All workflow modes, reasoning budgets, model tiers, and Definition of Done (DoD) profiles are governed by `framework.config.yaml`.
- 📁 **Centralized Work-Item Registry**: Work artifacts, design specs, test plans, and verification logs are stored centrally on your system under a single root.
- 🔄 **Execution-Verification Loop**: Enforces that every change is validated by running tests, lints, and builds locally. No "done" claim is accepted without pasted verification evidence.
- 🛡️ **Autonomy Dial & Safety Controls**: Set agent autonomy levels (L1/L2/L3) and enforce hard rules requiring manual human confirmation for high-risk actions (e.g. database schema changes, authentication updates).
- 🧠 **Self-Evolving Framework**: Learns your coding preferences, workflow patterns, and decision tendencies over time — applying them silently for low-risk choices and surfacing them as defaults for medium-risk ones. High-criticality decisions (security, auth, data) always require your explicit confirmation. The goal is to become your software engineering twin.
- 🔌 **MCP Tool Discovery & Self-Install**: Detects capability gaps for each task, researches the best-suited MCP tools from known registries, presents a recommendation, and self-installs upon your approval — so the agent is always optimally equipped.

---

## Directory Structure

```text
saarthi/
├── saarthi.agent.md                     # Main custom agent configuration (tool-agnostic)
├── saarthi-publish-to-central.prompt.md  # Slash command prompt to publish framework updates
├── work-item-kickoff.prompt.md          # Slash command prompt to initiate new tasks
├── pilot-checklist.prompt.md            # Slash command prompt to verify repository readiness
└── saarthi-framework/                   # The framework source directory
    ├── AGENTS.md                        # Repository instructions for the agent framework
    ├── framework.config.yaml            # Machine-readable budgets, safety rules, and DoD
    ├── _framework/                      # Governing policies, Index router, and entry prompts
    │   ├── 16-adaptive-learning.md      # Self-evolution: learning user preferences over time
    │   └── 17-mcp-tool-discovery.md     # MCP tool gap detection, research, and self-install
    ├── templates/                       # Markdown templates for design, implementation, and QA
    ├── tools/                           # Verification and smoke-testing scripts
    ├── knowledge-base/                  # Persistent learned preferences, patterns, and ADRs
    └── work-items/                      # Active and completed work items
```

---

## Quick Start

### Prerequisites
- **Python 3** (for validation, schema checks, and smoke-test scripts)
- Any supported AI coding tool (see installation guide below)

### Installation Guide

Saarthi is **agent-agnostic** — the same framework files work with any AI coding
tool. Copy the same set of files to the tool-specific location for your editor.

**Files to copy (identical for all tools):**
```text
saarthi.agent.md
work-item-kickoff.prompt.md
saarthi-publish-to-central.prompt.md
pilot-checklist.prompt.md              (optional)
saarthi-framework/                     (entire folder)
```

---

#### GitHub Copilot (VS Code)

1. Locate your VS Code user prompts folder:
   - **Windows:** `%APPDATA%\Code\User\prompts`
   - **macOS:** `~/Library/Application Support/Code/User/prompts`
   - **Linux:** `~/.config/Code/User/prompts`
2. Copy all files above into that folder.
3. Reload VS Code (`Developer: Reload Window`).
4. Open Copilot Chat — the **सारथी (Saarthi)** custom agent and slash commands (`/work-item-kickoff`, `/saarthi-publish-to-central`) will appear.

---

#### Cursor

**Option A — Global (recommended):**
1. Copy all files into `~/.cursor/prompts/` (create if missing).

**Option B — Per-project:**
1. Copy `saarthi-framework/` into your project root.
2. Create `.cursor/rules/saarthi.mdc` referencing the framework.

The framework loads automatically when you start an AI conversation in Cursor.

---

#### Claude Code (CLI)

1. Copy all files into `~/.config/claude/` (recommended):
   ```bash
   cp saarthi.agent.md work-item-kickoff.prompt.md \
      saarthi-publish-to-central.prompt.md ~/.config/claude/
   cp -r saarthi-framework ~/.config/claude/
   ```
2. Add `saarthi-framework/AGENTS.md` to your project root **or** append its contents to your global `~/.config/claude/CLAUDE.md`.
3. Claude Code reads `AGENTS.md` automatically in any project that contains it.

---

#### GitHub Copilot CLI (`gh copilot`)

1. Place `saarthi-framework/` in a known directory (e.g. `~/saarthi-framework`).
2. Create a shell alias for convenience:
   ```bash
   alias saarthi='gh copilot suggest --target shell'
   ```
3. At the start of a session, paste the distilled entry prompt:
   ```bash
   cat ~/saarthi-framework/_framework/00a-distilled-entry-prompt.txt
   ```

---

#### Windsurf

1. Copy all files into `~/.windsurf/prompts/` (create if missing) **or** into your project root.
2. Open Windsurf. In the Cascade panel, activate Saarthi:
   ```
   Load the Saarthi framework from <framework-home>/AGENTS.md
   ```

---

#### Cline / Continue / Other tools

1. Copy `saarthi-framework/` to a known path (e.g. `~/saarthi-framework`).
2. Place `saarthi-framework/AGENTS.md` in your project root (rename to the tool's equivalent instruction file if needed).
3. Configure the tool's **Custom Instructions** or **System Prompt** to include the contents of `_framework/00-single-entry-prompt.md`.

---

#### Antigravity / Antigravity CLI

1. Copy `saarthi-framework/` into your workspace directory (it is read automatically from the repository root via `AGENTS.md`).
2. For Antigravity CLI:
   ```bash
   antigravity run --system-prompt saarthi-framework/_framework/00-single-entry-prompt.md
   ```

---

#### Validate your installation (all tools)

```bash
python saarthi-framework/tools/smoke_test_framework.py --root saarthi-framework
python saarthi-framework/tools/validate_framework.py --root saarthi-framework
```
Expected: `SMOKE TEST PASSED` and `FRAMEWORK VALIDATION PASSED`

For detailed per-tool instructions, see [saarthi-framework/SETUP-CHECKLIST.txt](saarthi-framework/SETUP-CHECKLIST.txt).

---

## Daily Workflow

### Phase 1: Intake & Kickoff
Initialize a work item by invoking the **सारथी (Saarthi)** agent with `/work-item-kickoff` or by entering:
```text
Work Item ID: JIRA-1234
Requirement: Create an API endpoint to generate CSV exports of order history.
```
The agent will automatically create the folder `work-items/JIRA-1234/`, classify the task risk, choose the lightest safe workflow mode, and request answers to blocking questions.

### Phase 2: Implementation & Verification
As changes are implemented, the agent runs the execution-verification loop:
1. Running build, lint, and tests.
2. Collecting execution logs.
3. Troubleshooting any errors until the entire test suite passes.

### Phase 3: Done Validation
Before the agent claims a task is "done", verify the work item by running:
```bash
python saarthi-framework/tools/validate_work_item.py JIRA-1234 --root saarthi-framework
```
A successful validation (exit code `0`) is required to close the work item.

---

## License

This framework is licensed under a split **Personal / Commercial License**:
- **Personal Use**: Free and open to everyone for personal, educational, and non-commercial projects.
- **Commercial Use**: Use by organizations, freelancers, or individuals for commercial benefit requires purchasing a commercial license.

See the [LICENSE](LICENSE) file for the full legal terms.
