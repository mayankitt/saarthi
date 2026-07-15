#!/usr/bin/env zsh
set -euo pipefail

SCRIPT_DIR="$( cd "$( dirname "$0" )" >/dev/null 2>&1 && pwd )"
DEFAULT_DEST="$( cd "$SCRIPT_DIR/.." >/dev/null 2>&1 && pwd )"

SOURCE_PATH="${1:-}"
DESTINATION_PATH="${2:-$DEFAULT_DEST}"
FORCE_FLAG="${3:-}"

if [[ -z "$SOURCE_PATH" ]]; then
  echo "Usage: publish-framework.zsh <SourcePath> [DestinationPath] [--force]"
  exit 64
fi
if [[ "${2:-}" == "--force" ]]; then
  DESTINATION_PATH="$DEFAULT_DEST"
  FORCE_FLAG="--force"
fi

if [[ ! -e "$SOURCE_PATH" ]]; then
  echo "Source path not found: $SOURCE_PATH"
  exit 1
fi

src_full="$(cd "$SOURCE_PATH" && pwd)"
mkdir -p "$DESTINATION_PATH"
dest_full="$(cd "$DESTINATION_PATH" && pwd)"

if [[ "$src_full" == "$dest_full" ]]; then
  echo "Source and destination are the same path."
  exit 1
fi

signature=(
  "framework.config.yaml"
  "manifest.json"
  "AGENTS.md"
  "_framework"
  "templates"
  "tools"
)

found=0
for rel in "${signature[@]}"; do
  if [[ -e "$SOURCE_PATH/$rel" ]]; then
    ((found+=1))
  fi
done

score=$(( found * 100 / ${#signature[@]} ))
if [[ $score -lt 50 && "$FORCE_FLAG" != "--force" ]]; then
  echo "Guardrail: source path looks very different from expected framework structure."
  echo "Source: $SOURCE_PATH"
  echo "Similarity score: ${score}% (threshold: 50%)"
  read "confirm?Proceed anyway? Type YES to continue: "
  if [[ "$confirm" != "YES" ]]; then
    echo "Publish cancelled by guardrail."
    exit 1
  fi
fi

find "$DESTINATION_PATH" -mindepth 1 -maxdepth 1 -exec rm -rf {} +
cp -R "$SOURCE_PATH"/. "$DESTINATION_PATH"/

missing=0
[[ -e "$DESTINATION_PATH/framework.config.yaml" ]] || missing=1
[[ -e "$DESTINATION_PATH/_framework/INDEX.md" ]] || missing=1
[[ -e "$DESTINATION_PATH/tools/validate-work-item.js" ]] || missing=1

if [[ $missing -ne 0 ]]; then
  echo "Publish completed, but required files are missing."
  exit 2
fi

echo "Publish successful."
echo "Source:      $SOURCE_PATH"
echo "Destination: $DESTINATION_PATH"
echo "Validator:   node \"$DESTINATION_PATH/tools/validate-work-item.js\" <WORK_ITEM_ID> --root \"$DESTINATION_PATH\""
if [[ "$FORCE_FLAG" == "--force" ]]; then
  echo "Guardrail override was used (--force)."
fi

echo "Running post-publish smoke test..."
if [[ -e "$DESTINATION_PATH/tools/smoke-test-framework.js" ]]; then
  node "$DESTINATION_PATH/tools/smoke-test-framework.js" --root "$DESTINATION_PATH"
else
  echo "Smoke-test helper not found after publish; running fallback smoke check."
  node "$DESTINATION_PATH/tools/validate-work-item.js" --help >/dev/null
fi

echo "Post-publish smoke test passed."
