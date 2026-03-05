#!/bin/bash
set -e

WORKDIR="/home/hsieh89t/.openclaw/workspace/config"
OUTFILE="$1"
PROMPT="$2"

if [ -z "$OUTFILE" ] || [ -z "$PROMPT" ]; then
  echo 'Usage: qwen_to_file.sh <output_file_rel_path> "<prompt>"'
  echo 'Example: qwen_to_file.sh notes/test.md "幫我寫一段... "'
  exit 1
fi

cd "$WORKDIR" || exit 1
mkdir -p "$(dirname "$OUTFILE")"

python3 "$WORKDIR/scripts/qwen_client.py" "$PROMPT" > "$OUTFILE"
echo "Wrote: $WORKDIR/$OUTFILE"
