#!/usr/bin/env bash
set -u

refresh_seconds="${1:-3}"
paused=0

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

while true; do
  clear

  host_name="$(hostname)"
  os_name="$(grep '^PRETTY_NAME=' /etc/os-release 2>/dev/null | cut -d= -f2- | tr -d '"')"
  kernel_ver="$(uname -r)"
  up_time="$(uptime -p 2>/dev/null || echo '-')"
  ip_addr="$(hostname -I 2>/dev/null | awk '{print $1}')"

  cpu_load="$(uptime | sed 's/.*load average: //')"
  mem_line="$(free -h | awk '/Mem:/ {print $3" / "$2"（可用 "$7"）"}')"
  swap_line="$(free -h | awk '/Swap:/ {print $3" / "$2}')"
  disk_root="$(df -h / | awk 'NR==2 {print $3" / "$2"（已用 "$5"）"}')"

  ollama_state="$(systemctl is-active ollama 2>/dev/null || echo unknown)"
  gateway_state="$(systemctl --user is-active openclaw-gateway 2>/dev/null || echo unknown)"
  ollama_pid="$(systemctl show -p MainPID --value ollama 2>/dev/null || echo -)"
  gateway_pid="$(systemctl --user show -p MainPID --value openclaw-gateway 2>/dev/null || echo -)"

  ports_summary="$(ss -ltn 2>/dev/null | awk 'NR>1 {split($4,a,":"); p=a[length(a)]; if(p!="") c[p]++} END {n=0; for (k in c) {printf "%s%s", (n?", ":""), k; n++; if(n>=8) break} if(n==0) printf "無"}')"

  echo "================= 電腦健康總覽（精簡）================="
  echo "時間：$(date '+%Y-%m-%d %H:%M:%S %Z')"
  echo "主機：$host_name | IP：${ip_addr:--}"
  echo "系統：$os_name"
  echo "核心：$kernel_ver | 開機時長：$up_time"
  echo
  echo "【資源】"
  echo "CPU 負載：$cpu_load"
  echo "記憶體：$mem_line"
  echo "Swap：$swap_line"
  echo "磁碟 / ：$disk_root"
  echo
  echo "【服務】"
  echo "Ollama：$(status_zh "$ollama_state")（PID: $ollama_pid）"
  echo "OpenClaw Gateway：$(status_zh "$gateway_state")（PID: $gateway_pid）"
  echo
  echo "【監聽埠（前8）】${ports_summary}"
  echo
  echo "【CPU 前3 程序】"
  ps -eo comm,%cpu,%mem --sort=-%cpu | sed -n '2,4p' | awk '{printf "- %-20s CPU:%5s%% MEM:%5s%%\n", $1, $2, $3}'
  echo

  if [[ "$paused" -eq 1 ]]; then
    echo "狀態：已暫停更新（按 p 繼續｜q 離開）"
    read -rsn1 key
  else
    echo "每 ${refresh_seconds} 秒更新｜p 暫停｜q 離開"
    read -rsn1 -t "$refresh_seconds" key || key=""
  fi

  case "$key" in
    p|P)
      if [[ "$paused" -eq 1 ]]; then
        paused=0
      else
        paused=1
      fi
      ;;
    q|Q)
      break
      ;;
  esac
done
