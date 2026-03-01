#!/bin/bash
cd /home/hsieh89t/.openclaw/workspace/config || exit

git add .
if ! git diff --cached --quiet; then
  git commit -m "auto backup $(date '+%Y-%m-%d %H:%M:%S')"
  git push origin main
fi
