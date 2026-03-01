#!/bin/bash
set -e

WORKSPACE="/home/hsieh89t/.openclaw/workspace"
PROMPT_FILE="$WORKSPACE/daily_monitor_prompt.md"

# Read the prompt
TASK=$(cat "$PROMPT_FILE")

# Run agent with the task
openclaw agent --agent main --message "$TASK" --thinking medium --timeout 1800