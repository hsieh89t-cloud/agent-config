#!/bin/bash
set -euo pipefail

WORKDIR="/home/hsieh89t/.openclaw/workspace"
CONFIG="$WORKDIR/config/deepseek_config.json"
SUMMARY_FILE="$WORKDIR/context/session_summary.md"

if [[ ! -f "$CONFIG" ]]; then
  echo "[錯誤] 找不到 $CONFIG ，請先執行 switch_deepseek.py 建立設定。"
  exit 1
fi

if [[ $# -eq 0 ]]; then
  echo "使用方式： ./run_deepseek.sh \"你的提問\""
  exit 1
fi

PROMPT="$*"

MODEL=$(jq -r '.model' "$CONFIG")
ENDPOINT=$(jq -r '.endpoint' "$CONFIG")
AUTH_HEADER=$(jq -r '.headers.Authorization' "$CONFIG")

if [[ -z "$MODEL" || -z "$ENDPOINT" || -z "$AUTH_HEADER" ]]; then
  echo "[錯誤] deepseek_config.json 資訊不完整。"
  exit 1
fi

SYSTEM_MSG="你是一個以繁體中文回答的 AI 助理，請保持重點式、簡潔，避免冗長描述。若提供程式碼，僅顯示必要片段。"

if [[ -s "$SUMMARY_FILE" ]]; then
  SUMMARY_CONTENT=$(cat "$SUMMARY_FILE")
  SYSTEM_MSG+=$'\n\n以下為對話壓縮摘要，請視為已知背景：\n'
  SYSTEM_MSG+="$SUMMARY_CONTENT"
fi

PAYLOAD=$(jq -n --arg model "$MODEL" \
              --arg system "$SYSTEM_MSG" \
              --arg user "$PROMPT" \
              --argjson temperature 0.3 \
              --argjson max_tokens 600 \
              '{model: $model,
                temperature: $temperature,
                max_tokens: $max_tokens,
                messages: [
                  {role: "system", content: $system},
                  {role: "user", content: $user}
                ]}')

RESPONSE=$(curl -sS "$ENDPOINT" \
  -H "Content-Type: application/json" \
  -H "Authorization: $AUTH_HEADER" \
  -d "$PAYLOAD")

ERROR=$(echo "$RESPONSE" | jq -r '.error.message? // empty')
if [[ -n "$ERROR" ]]; then
  echo "[DeepSeek API 錯誤] $ERROR"
  exit 1
fi

echo "$RESPONSE" | jq -r '.choices[0].message.content'
