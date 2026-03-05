#!/bin/bash
set -e

WORKDIR="/home/hsieh89t/.openclaw/workspace/config"
cd "$WORKDIR" || exit 1

echo "=== Agent Auto Backup ==="

git add .

# Preflight: block sensitive files from being committed
STAGED="$(git diff --cached --name-only || true)"
if echo "$STAGED" | grep -E -i '(^|/)\.env$|token|secret|credentials|(^|/)secrets/|(^|/)id_rsa$|(^|/)id_ed25519$|(^|/)\.ssh(/|$)' >/dev/null; then
  echo "⚠️  Aborted: sensitive file pattern detected in staged changes:"
  echo "$STAGED" | grep -E -i '(^|/)\.env$|token|secret|credentials|(^|/)secrets/|(^|/)id_rsa$|(^|/)id_ed25519$|(^|/)\.ssh(/|$)' || true
  echo "Fix .gitignore or remove those files, then retry."
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
