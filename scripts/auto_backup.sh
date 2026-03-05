#!/bin/bash

WORKDIR="/home/ysga/.openclaw/workspace/config"

cd "$WORKDIR" || exit 1

echo "=== Agent Auto Backup ==="

git add .

# Preflight sensitive-file check on staged files
STAGED_FILES=$(git diff --cached --name-only)
echo "Staged files:"
echo "$STAGED_FILES"

if echo "$STAGED_FILES" | grep -Ei '(^|/)(\.env|.*token.*|.*secret.*|.*credentials.*|secrets/.*|id_rsa|id_ed25519|\.ssh($|/))' >/tmp/backup_sensitive_hits.txt; then
  echo "[BLOCKED] Sensitive pattern detected in staged files:"
  cat /tmp/backup_sensitive_hits.txt
  exit 2
fi

if git diff --cached --quiet; then
 echo "No changes detected."
else
 COMMIT_MSG="auto backup $(date '+%Y-%m-%d %H:%M:%S')"
 git commit -m "$COMMIT_MSG"
 git push origin main
 echo "Backup pushed."
fi

echo "=== Done ==="
