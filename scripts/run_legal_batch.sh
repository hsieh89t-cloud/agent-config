#!/bin/bash
# 法律條文批次處理 - 定時執行腳本
# 每天凌晨2點執行

# 設定環境變數
export PATH="/home/ysga/.local/bin:/home/ysga/.npm-global/bin:/home/ysga/bin:/usr/local/bin:/usr/bin:/bin"
export HOME="/home/ysga"
export LANG="zh_TW.UTF-8"
export LC_ALL="zh_TW.UTF-8"

# 設定工作目錄
cd /home/ysga/.openclaw/workspace

# 建立日誌目錄
mkdir -p logs
mkdir -p batch_outputs

# 日誌文件
LOG_FILE="logs/legal_batch_$(date +%Y%m%d_%H%M%S).log"
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

echo "================================================" >> "$LOG_FILE"
echo "法律條文批次處理開始時間: $TIMESTAMP" >> "$LOG_FILE"
echo "================================================" >> "$LOG_FILE"

# 檢查Ollama服務
echo "檢查Ollama服務狀態..." >> "$LOG_FILE"
if curl -s http://127.0.0.1:11434/api/tags > /dev/null; then
    echo "✓ Ollama服務正常" >> "$LOG_FILE"
else
    echo "✗ Ollama服務未啟動，嘗試啟動..." >> "$LOG_FILE"
    # 嘗試啟動Ollama（後台執行）
    ollama serve > /dev/null 2>&1 &
    sleep 10
    
    if curl -s http://127.0.0.1:11434/api/tags > /dev/null; then
        echo "✓ Ollama啟動成功" >> "$LOG_FILE"
    else
        echo "✗ 無法啟動Ollama，退出處理" >> "$LOG_FILE"
        exit 1
    fi
fi

# 執行批次處理（每個法域處理10條）
echo "開始批次處理..." >> "$LOG_FILE"

# 1. 處理刑法（20條）
echo "處理刑法..." >> "$LOG_FILE"
python3 scripts/legal_batch_processor_v4.py \
    --input "/home/ysga/文件/Obsidian Vault/00_資料收集/法律資料庫_三法分流/03_刑法/來源資料/刑法.csv" \
    --output-dir "/home/ysga/文件/Obsidian Vault/00_資料收集/法律資料庫_三法分流/03_刑法/索引輸出" \
    --limit 20 \
    --batch-name "刑法批次" >> "$LOG_FILE" 2>&1

刑法結果=$?
if [ $刑法結果 -eq 0 ]; then
    echo "✓ 刑法處理完成" >> "$LOG_FILE"
else
    echo "✗ 刑法處理失敗" >> "$LOG_FILE"
fi

# 生成刑法重跑清單
echo "生成刑法重跑清單..." >> "$LOG_FILE"
python3 scripts/generate_rerun_list.py \
    "/home/ysga/文件/Obsidian Vault/00_資料收集/法律資料庫_三法分流/03_刑法/索引輸出" \
    "刑法批次" >> "$LOG_FILE" 2>&1

刑法重跑結果=$?
if [ $刑法重跑結果 -eq 0 ]; then
    echo "✓ 刑法重跑清單生成完成" >> "$LOG_FILE"
else
    echo "✗ 刑法重跑清單生成失敗" >> "$LOG_FILE"
fi

# 短暫暫停
sleep 5

# 2. 處理民法（20條）
echo "處理民法..." >> "$LOG_FILE"
python3 scripts/legal_batch_processor_v4.py \
    --input "/home/ysga/文件/Obsidian Vault/00_資料收集/法律資料庫_三法分流/02_民法/來源資料/民法.csv" \
    --output-dir "/home/ysga/文件/Obsidian Vault/00_資料收集/法律資料庫_三法分流/02_民法/索引輸出" \
    --limit 20 \
    --batch-name "民法批次" >> "$LOG_FILE" 2>&1

民法結果=$?
if [ $民法結果 -eq 0 ]; then
    echo "✓ 民法處理完成" >> "$LOG_FILE"
else
    echo "✗ 民法處理失敗" >> "$LOG_FILE"
fi

# 生成民法重跑清單
echo "生成民法重跑清單..." >> "$LOG_FILE"
python3 scripts/generate_rerun_list.py \
    "/home/ysga/文件/Obsidian Vault/00_資料收集/法律資料庫_三法分流/02_民法/索引輸出" \
    "民法批次" >> "$LOG_FILE" 2>&1

民法重跑結果=$?
if [ $民法重跑結果 -eq 0 ]; then
    echo "✓ 民法重跑清單生成完成" >> "$LOG_FILE"
else
    echo "✗ 民法重跑清單生成失敗" >> "$LOG_FILE"
fi

# 短暫暫停
sleep 5

# 3. 處理憲法（20條）
echo "處理憲法..." >> "$LOG_FILE"
python3 scripts/legal_batch_processor_v4.py \
    --input "/home/ysga/文件/Obsidian Vault/00_資料收集/法律資料庫_三法分流/01_憲法/來源資料/憲法.csv" \
    --output-dir "/home/ysga/文件/Obsidian Vault/00_資料收集/法律資料庫_三法分流/01_憲法/索引輸出" \
    --limit 20 \
    --batch-name "憲法批次" >> "$LOG_FILE" 2>&1

憲法結果=$?
if [ $憲法結果 -eq 0 ]; then
    echo "✓ 憲法處理完成" >> "$LOG_FILE"
else
    echo "✗ 憲法處理失敗" >> "$LOG_FILE"
fi

# 生成憲法重跑清單
echo "生成憲法重跑清單..." >> "$LOG_FILE"
python3 scripts/generate_rerun_list.py \
    "/home/ysga/文件/Obsidian Vault/00_資料收集/法律資料庫_三法分流/01_憲法/索引輸出" \
    "憲法批次" >> "$LOG_FILE" 2>&1

憲法重跑結果=$?
if [ $憲法重跑結果 -eq 0 ]; then
    echo "✓ 憲法重跑清單生成完成" >> "$LOG_FILE"
else
    echo "✗ 憲法重跑清單生成失敗" >> "$LOG_FILE"
fi

# 生成總體重跑摘要
echo "生成總體重跑摘要..." >> "$LOG_FILE"
RERUN_SUMMARY_DIR="/home/ysga/文件/Obsidian Vault/00_資料收集/法律資料庫_三法分流/重跑清單"
mkdir -p "$RERUN_SUMMARY_DIR"

# 收集所有重跑清單
RERUN_LISTS=()
for dir in "/home/ysga/文件/Obsidian Vault/00_資料收集/法律資料庫_三法分流/03_刑法/索引輸出" \
           "/home/ysga/文件/Obsidian Vault/00_資料收集/法律資料庫_三法分流/02_民法/索引輸出" \
           "/home/ysga/文件/Obsidian Vault/00_資料收集/法律資料庫_三法分流/01_憲法/索引輸出"; do
    latest_rerun=$(find "$dir" -name "*_rerun_*.csv" -type f | sort -r | head -1)
    if [ -n "$latest_rerun" ]; then
        RERUN_LISTS+=("$latest_rerun")
    fi
done

if [ ${#RERUN_LISTS[@]} -gt 0 ]; then
    echo "找到重跑清單: ${RERUN_LISTS[*]}" >> "$LOG_FILE"
    
    # 調用Python生成總體摘要
    python3 scripts/generate_overall_rerun_summary.py "${RERUN_LISTS[@]}" "$RERUN_SUMMARY_DIR" >> "$LOG_FILE" 2>&1
    
    if [ $? -eq 0 ]; then
        echo "✓ 總體重跑摘要生成完成" >> "$LOG_FILE"
    else
        echo "✗ 總體重跑摘要生成失敗" >> "$LOG_FILE"
    fi
else
    echo "沒有需要重跑的條目" >> "$LOG_FILE"
fi

# 生成日報告
TIMESTAMP_END=$(date "+%Y-%m-%d %H:%M:%S")
echo "================================================" >> "$LOG_FILE"
echo "法律條文批次處理結束時間: $TIMESTAMP_END" >> "$LOG_FILE"
echo "總計處理: 刑法($刑法結果) 民法($民法結果) 憲法($憲法結果)" >> "$LOG_FILE"
if [ ${#RERUN_LISTS[@]} -gt 0 ]; then
    echo "需要重跑: 有 ${#RERUN_LISTS[@]} 個清單" >> "$LOG_FILE"
else
    echo "需要重跑: 無" >> "$LOG_FILE"
fi
echo "================================================" >> "$LOG_FILE"

# 檢查輸出文件
echo "檢查輸出文件..." >> "$LOG_FILE"
echo "刑法輸出:" >> "$LOG_FILE"
ls -la "/home/ysga/文件/Obsidian Vault/00_資料收集/法律資料庫_三法分流/03_刑法/索引輸出"/*.csv 2>/dev/null | head -3 >> "$LOG_FILE"
echo "民法輸出:" >> "$LOG_FILE"
ls -la "/home/ysga/文件/Obsidian Vault/00_資料收集/法律資料庫_三法分流/02_民法/索引輸出"/*.csv 2>/dev/null | head -3 >> "$LOG_FILE"
echo "憲法輸出:" >> "$LOG_FILE"
ls -la "/home/ysga/文件/Obsidian Vault/00_資料收集/法律資料庫_三法分流/01_憲法/索引輸出"/*.csv 2>/dev/null | head -3 >> "$LOG_FILE"

# 發送通知（可選）
# 這裡可以添加發送通知的程式碼，例如發送郵件或Telegram通知

echo "批次處理完成!" >> "$LOG_FILE"

# 保留最新的10個日誌文件
cd logs
ls -t legal_batch_*.log | tail -n +11 | xargs rm -f 2>/dev/null || true

exit 0