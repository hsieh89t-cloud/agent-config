#!/usr/bin/env bash
set -u

REFRESH_SECONDS="${1:-3}"

while true; do
  clear
  echo "================= 智研系統儀表板 ================="
  echo "時間: $(date '+%F %T %Z')"
  echo

  echo "[服務狀態]"
  OLLAMA_STATE=$(systemctl is-active ollama 2>/dev/null || echo unknown)
  GW_STATE=$(systemctl --user is-active openclaw-gateway 2>/dev/null || echo unknown)
  OLLAMA_PID=$(systemctl show -p MainPID --value ollama 2>/dev/null || echo -)
  GW_PID=$(systemctl --user show -p MainPID --value openclaw-gateway 2>/dev/null || echo -)
  echo "- Ollama           : ${OLLAMA_STATE} (PID: ${OLLAMA_PID})"
  echo "- OpenClaw Gateway : ${GW_STATE} (PID: ${GW_PID})"
  echo

  echo "[OpenClaw 快照]"
  openclaw gateway status 2>/dev/null | sed -n '1,14p'
  echo

  echo "[系統資源]"
  echo "- CPU Load : $(uptime | sed 's/.*load average: //')"
  echo "- Memory   : $(free -h | awk '/Mem:/ {print $3" / "$2" (free "$4")"}')"
  echo "- Disk /   : $(df -h / | awk 'NR==2 {print $3" / "$2" ("$5" used)"}')"
  echo

  echo "[最近 OpenClaw 日誌]"
  LOG_FILE=$(ls -1t /tmp/openclaw/openclaw-*.log 2>/dev/null | head -n 1)
  if [[ -n "${LOG_FILE:-}" ]]; then
    tail -n 8 "$LOG_FILE"
  else
    echo "(找不到 /tmp/openclaw/openclaw-*.log)"
  fi

  echo
  echo "--------------------------------------------------"
  echo "每 ${REFRESH_SECONDS} 秒更新；Ctrl+C 離開"
  sleep "$REFRESH_SECONDS"
done
