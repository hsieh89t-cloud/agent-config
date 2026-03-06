#!/usr/bin/env bash
set -u

更新秒數="${1:-3}"

狀態中文() {
  case "$1" in
    active) echo "運行中" ;;
    inactive) echo "未運行" ;;
    failed) echo "失敗" ;;
    activating) echo "啟動中" ;;
    deactivating) echo "停止中" ;;
    *) echo "$1" ;;
  esac
}

while true; do
  clear
  echo "================= 智研系統儀表板 ================="
  echo "現在時間：$(date '+%Y-%m-%d %H:%M:%S %Z')"
  echo

  echo "【服務狀態】"
  OLLAMA_STATE_RAW=$(systemctl is-active ollama 2>/dev/null || echo unknown)
  GW_STATE_RAW=$(systemctl --user is-active openclaw-gateway 2>/dev/null || echo unknown)
  OLLAMA_PID=$(systemctl show -p MainPID --value ollama 2>/dev/null || echo -)
  GW_PID=$(systemctl --user show -p MainPID --value openclaw-gateway 2>/dev/null || echo -)

  OLLAMA_STATE=$(狀態中文 "$OLLAMA_STATE_RAW")
  GW_STATE=$(狀態中文 "$GW_STATE_RAW")

  echo "- Ollama 服務        ：${OLLAMA_STATE}（PID：${OLLAMA_PID}）"
  echo "- OpenClaw Gateway   ：${GW_STATE}（PID：${GW_PID}）"
  echo

  echo "【OpenClaw 快照（摘要）】"
  openclaw gateway status 2>/dev/null | sed -n '1,14p'
  echo

  echo "【系統資源】"
  echo "- CPU 平均負載：$(uptime | sed 's/.*load average: //')"
  echo "- 記憶體使用量：$(free -h | awk '/Mem:/ {print $3" / "$2"（可用 "$7"）"}')"
  echo "- 磁碟使用量(/)：$(df -h / | awk 'NR==2 {print $3" / "$2"（已用 "$5"）"}')"
  echo

  echo "【最近 OpenClaw 日誌（最後 8 行）】"
  LOG_FILE=$(ls -1t /tmp/openclaw/openclaw-*.log 2>/dev/null | head -n 1)
  if [[ -n "${LOG_FILE:-}" ]]; then
    echo "日誌檔案：$LOG_FILE"
    tail -n 8 "$LOG_FILE"
  else
    echo "（找不到 /tmp/openclaw/openclaw-*.log）"
  fi

  echo
  echo "--------------------------------------------------"
  echo "每 ${更新秒數} 秒自動更新；按 Ctrl + C 離開"
  sleep "$更新秒數"
done
