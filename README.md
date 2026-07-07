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

---

## Directory Structure

```text
saarthi/
├── saarthi.agent.md                     # Main custom agent configuration for your IDE
├── saarthi-publish-to-central.prompt.md  # Slash command prompt to publish framework updates
├── work-item-kickoff.prompt.md          # Slash command prompt to initiate new tasks
├── pilot-checklist.prompt.md            # Slash command prompt to verify repository readiness
└── saarthi-framework/                   # The framework source directory
    ├── AGENTS.md                        # Repository instructions for the agent framework
    ├── framework.config.yaml            # Machine-readable budgets, safety rules, and DoD
    ├── _framework/                      # Governing policies, Index router, and entry prompts
    ├── templates/                       # Markdown templates for design, implementation, and QA
    ├── tools/                           # Verification and smoke-testing scripts
    └── work-items/                      # Active and completed work items
```

---

## Quick Start

### 1. Prerequisites
- **VS Code** (or any agent-supported editor)
- **Node.js** (for running verification scripts)
- **GitHub Copilot** or a similar agentic extension

### 2. Setup
For detailed instructions, refer to [saarthi-framework/SETUP-CHECKLIST.txt](saarthi-framework/SETUP-CHECKLIST.txt). 

In short:
1. Locate your editor's user prompts directory (e.g., `%APPDATA%\Code\User\prompts` on Windows).
2. Copy `saarthi.agent.md`, `saarthi-publish-to-central.prompt.md`, `work-item-kickoff.prompt.md`, `pilot-checklist.prompt.md`, and the `saarthi-framework/` directory into that prompts folder.
3. Reload your editor. The **सारथी (Saarthi)** custom agent and slash commands will appear in your chat assistant.

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
node saarthi-framework/tools/validate-work-item.js JIRA-1234
```
A successful validation (exit code `0`) is required to close the work item.

---

## License

This framework is licensed under a split **Personal / Commercial License**:
- **Personal Use**: Free and open to everyone for personal, educational, and non-commercial projects.
- **Commercial Use**: Use by organizations, freelancers, or individuals for commercial benefit requires purchasing a commercial license.

See the [LICENSE](LICENSE) file for the full legal terms.
