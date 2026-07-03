---
mode: ask
description: "Publish सारथी (Saarthi) framework changes from a working copy into the centralized source-of-truth and run health checks."
---

Publish **सारथी (Saarthi)** framework updates to the centralized source of truth.

Inputs:
- Source framework path (working copy): <absolute path>
- Destination (source of truth): <framework-home> (default auto-resolved by scripts)

Recommended publish methods:
- Windows (PowerShell):
  powershell -ExecutionPolicy Bypass -File "<framework-home>\tools\publish-framework.ps1" -SourcePath "<working-copy-path>"
- Windows (CMD):
  "<framework-home>\tools\publish-framework.bat" "<working-copy-path>"
- macOS/Linux (bash):
  bash "<framework-home>/tools/publish-framework.sh" "<working-copy-path>" "<framework-home>"
- macOS/Linux (zsh):
  zsh "<framework-home>/tools/publish-framework.zsh" "<working-copy-path>" "<framework-home>"

Guardrail behavior:
- If source structure looks vastly different from a framework root (similarity < 50%), stop and ask for explicit YES confirmation.
- Use `--force` only when intentional.

Steps:
1. Replace destination contents with source contents.
2. Validate required files exist:
   - framework.config.yaml
   - _framework/INDEX.md
   - tools/validate-work-item.js
3. Run post-publish smoke test automatically:
   - required-file checks
   - `node tools/validate-work-item.js --help`
4. Report publish + smoke-test status and any missing files.
5. Show validator command template:
   node "<destination>\tools\validate-work-item.js" <WORK_ITEM_ID> --root "<destination>"
