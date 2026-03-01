#!/bin/bash
WORKDIR="/home/hsieh89t/.openclaw/workspace/config"
cd "$WORKDIR" || exit 1

echo "=== Agent Auto Backup ==="
git add .

if git diff --cached --quiet; then
    echo "No changes detected."
else
    COMMIT_MSG="auto backup $(date '+%Y-%m-%d %H:%M:%S')"
    git commit -m "$COMMIT_MSG"
    git push origin main
    echo "Backup pushed."
fi

echo "=== Done ==="
