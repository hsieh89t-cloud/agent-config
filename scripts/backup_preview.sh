#!/bin/bash
cd /home/ysga/.openclaw/workspace/config || exit 1
git status
echo "----- DIFF -----"
git diff
