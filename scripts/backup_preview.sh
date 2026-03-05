#!/bin/bash
set -e
cd /home/hsieh89t/.openclaw/workspace/config || exit 1
git status
echo "----- DIFF -----"
git diff
