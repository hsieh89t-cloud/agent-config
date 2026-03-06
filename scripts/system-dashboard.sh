#!/usr/bin/env bash
set -u

refresh_seconds="${1:-3}"

status_zh() {
  case "$1" in
    active) echo "運行中" ;;
    inactive) echo "未運行" ;;
    failed) echo "失敗" ;;
    activating) echo "啟動中" ;;
    deactivating) echo "停止中" ;;
    *) echo "$1" ;;
  esac
}

get_cmd() {
  command -v "$1" >/dev/null 2>&1
}

while true; do
  clear
  echo "================= 電腦健康總覽儀表板 ================="
  echo "現在時間：$(date '+%Y-%m-%d %H:%M:%S %Z')"
  echo

  echo "【主機總覽】"
  echo "- 主機名稱：$(hostname)"
  echo "- 系統版本：$(grep '^PRETTY_NAME=' /etc/os-release 2>/dev/null | cut -d= -f2- | tr -d '"')"
  echo "- 核心版本：$(uname -r)"
  echo "- 開機時長：$(uptime -p 2>/dev/null || true)"
  echo

  echo "【資源健康】"
  echo "- CPU 平均負載：$(uptime | sed 's/.*load average: //')"
  echo "- 記憶體使用量：$(free -h | awk '/Mem:/ {print $3" / "$2"（可用 "$7"）"}')"
  echo "- Swap 使用量 ：$(free -h | awk '/Swap:/ {print $3" / "$2}')"
  echo "- 磁碟使用量(/)：$(df -h / | awk 'NR==2 {print $3" / "$2"（已用 "$5"）"}')"
  echo

  echo "【磁碟健康（空間前5）】"
  df -h | awk 'NR==1 || /^\/dev\// {print}' | head -n 6
  echo

  echo "【網路與連線】"
  echo "- 內網 IP：$(hostname -I 2>/dev/null | awk '{print $1}')"
  if get_cmd ss; then
    echo "- 監聽中的 TCP 埠（前10筆）："
    ss -ltn 2>/dev/null | sed -n '1,11p'
  else
    echo "- 無 ss 指令可顯示埠資訊"
  fi
  echo

  echo "【關鍵服務狀態】"
  OLLAMA_STATE_RAW=$(systemctl is-active ollama 2>/dev/null || echo unknown)
  GW_STATE_RAW=$(systemctl --user is-active openclaw-gateway 2>/dev/null || echo unknown)
  OLLAMA_PID=$(systemctl show -p MainPID --value ollama 2>/dev/null || echo -)
  GW_PID=$(systemctl --user show -p MainPID --value openclaw-gateway 2>/dev/null || echo -)
  echo "- Ollama 服務       ：$(status_zh "$OLLAMA_STATE_RAW")（PID：$OLLAMA_PID）"
  echo "- OpenClaw Gateway  ：$(status_zh "$GW_STATE_RAW")（PID：$GW_PID）"
  echo

  echo "【高資源程序（CPU 前5）】"
  ps -eo pid,comm,%cpu,%mem --sort=-%cpu | sed -n '1,6p'
  echo

  echo "【OpenClaw 最近日誌（最後 6 行）】"
  log_file=$(ls -1t /tmp/openclaw/openclaw-*.log 2>/dev/null | head -n 1)
  if [[ -n "${log_file:-}" ]]; then
    echo "日誌檔案：$log_file"
    tail -n 6 "$log_file"
  else
    echo "（找不到 /tmp/openclaw/openclaw-*.log）"
  fi

  echo
  echo "------------------------------------------------------"
  echo "每 ${refresh_seconds} 秒自動更新；按 Ctrl + C 離開"
  sleep "$refresh_seconds"
done
