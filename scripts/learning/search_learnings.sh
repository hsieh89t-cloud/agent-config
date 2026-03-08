#!/bin/bash
# 學習搜尋腳本 - 基於 Adaptive Learning Agent 設計理念

MEMORY_FILE="$HOME/.openclaw/workspace/MEMORY.md"

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 顯示使用說明
show_help() {
    echo -e "${CYAN}學習搜尋系統 - 基於 Adaptive Learning Agent 設計理念${NC}"
    echo "用法: $0 [選項] [搜尋詞]"
    echo ""
    echo "選項:"
    echo "  -c, --category CATEGORY  按類別搜尋 (technique, bug-fix, best-practice, ...)"
    echo "  -s, --source SOURCE      按來源搜尋 (user-correction, error-discovery, ...)"
    echo "  -t, --tag TAG            按標籤搜尋"
    echo "  -e, --errors             顯示未解決的錯誤"
    echo "  -r, --recent [N]         顯示最近的學習 (預設: 10)"
    echo "  -S, --stats              顯示學習統計"
    echo "  -h, --help               顯示此說明"
    echo ""
    echo "範例:"
    echo "  $0 JSON 解析             搜尋包含 'JSON 解析' 的學習"
    echo "  $0 -c technique          搜尋技術類別的學習"
    echo "  $0 -e                    顯示未解決的錯誤"
    echo "  $0 -r 5                  顯示最近 5 個學習"
    echo "  $0 -S                    顯示學習統計"
}

# 顯示學習統計
show_stats() {
    echo -e "${CYAN}=== 學習統計 ===${NC}"
    
    # 總學習數
    total_learnings=$(grep -c "\[L[0-9]\]" "$MEMORY_FILE" 2>/dev/null || echo "0")
    total_errors=$(grep -c "\[E[0-9]\]" "$MEMORY_FILE" 2>/dev/null || echo "0")
    
    # 類別分佈
    echo -e "${GREEN}總學習記錄:${NC} $total_learnings"
    echo -e "${GREEN}錯誤記錄:${NC} $total_errors"
    
    # 未解決錯誤
    unresolved=$(grep -c "狀態.*unresolved" "$MEMORY_FILE" 2>/dev/null || echo "0")
    resolved=$((total_errors - unresolved))
    
    echo -e "${YELLOW}已解決錯誤:${NC} $resolved"
    if [ "$unresolved" -gt 0 ]; then
        echo -e "${RED}未解決錯誤:${NC} $unresolved"
    else
        echo -e "${GREEN}未解決錯誤:${NC} $unresolved"
    fi
    
    # 類別統計
    echo -e "\n${CYAN}學習類別分佈:${NC}"
    for category in technique bug-fix best-practice constraint api-quirk error-handling optimization security; do
        count=$(grep -c "類別.*$category" "$MEMORY_FILE" 2>/dev/null || echo "0")
        if [ "$count" -gt 0 ]; then
            echo -e "  $category: $count"
        fi
    done
    
    # 來源統計
    echo -e "\n${CYAN}學習來源分佈:${NC}"
    for source in user-correction error-discovery successful-pattern user-feedback system-observation experimentation; do
        count=$(grep -c "來源.*$source" "$MEMORY_FILE" 2>/dev/null || echo "0")
        if [ "$count" -gt 0 ]; then
            echo -e "  $source: $count"
        fi
    done
    
    # 最近學習
    echo -e "\n${CYAN}最近學習活動:${NC}"
    recent_dates=$(grep -o "\[[0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}\]" "$MEMORY_FILE" | sort -u | tail -5)
    for date in $recent_dates; do
        count=$(grep -c "$date" "$MEMORY_FILE" 2>/dev/null || echo "0")
        echo -e "  $date: $count 個學習"
    done
}

# 搜尋學習
search_learnings() {
    local query="$1"
    local category="$2"
    local source="$3"
    local tag="$4"
    
    echo -e "${CYAN}=== 搜尋結果 ===${NC}"
    
    # 建立搜尋模式
    local search_pattern=""
    
    if [ -n "$query" ]; then
        search_pattern="$query"
    fi
    
    if [ -n "$category" ]; then
        if [ -n "$search_pattern" ]; then
            search_pattern="$search_pattern.*類別.*$category"
        else
            search_pattern="類別.*$category"
        fi
    fi
    
    if [ -n "$source" ]; then
        if [ -n "$search_pattern" ]; then
            search_pattern="$search_pattern.*來源.*$source"
        else
            search_pattern="來源.*$source"
        fi
    fi
    
    if [ -n "$tag" ]; then
        if [ -n "$search_pattern" ]; then
            search_pattern="$search_pattern.*標籤.*$tag"
        else
            search_pattern="標籤.*$tag"
        fi
    fi
    
    # 執行搜尋
    if [ -n "$search_pattern" ]; then
        grep -n -i "$search_pattern" "$MEMORY_FILE" | head -20 | while read -r line; do
            format_learning_line "$line"
        done
    else
        # 顯示所有學習（前20個）
        grep -n "\[L[0-9]\]\|\[E[0-9]\]" "$MEMORY_FILE" | head -20 | while read -r line; do
            format_learning_line "$line"
        done
    fi
    
    # 顯示結果數量
    local count=$(grep -c -i "$search_pattern" "$MEMORY_FILE" 2>/dev/null || echo "0")
    echo -e "\n${GREEN}找到 $count 個結果${NC}"
}

# 格式化學習行
format_learning_line() {
    local line="$1"
    local line_num=$(echo "$line" | cut -d: -f1)
    local content=$(echo "$line" | cut -d: -f2-)
    
    # 判斷是學習還是錯誤
    if echo "$content" | grep -q "\[L[0-9]\]"; then
        # 學習記錄
        local id=$(echo "$content" | grep -o "\[L[0-9]\{3\}\]")
        local category=$(echo "$content" | grep -o "類別.*[^|]*" | cut -d'|' -f1 | sed 's/類別.*//' | xargs || echo "未知")
        
        echo -e "${GREEN}$id${NC} (行: $line_num)"
        echo -e "  ${BLUE}類別:${NC} $category"
        echo -e "  ${YELLOW}內容:${NC} $(echo "$content" | sed 's/.*|//' | head -1 | cut -d'|' -f1 | xargs)"
        echo ""
    elif echo "$content" | grep -q "\[E[0-9]\]"; then
        # 錯誤記錄
        local id=$(echo "$content" | grep -o "\[E[0-9]\{3\}\]")
        local status=$(echo "$content" | grep -o "狀態.*[^|]*" | cut -d'|' -f1 | sed 's/狀態.*//' | xargs || echo "未知")
        
        if echo "$status" | grep -qi "resolved"; then
            echo -e "${GREEN}$id${NC} (行: $line_num) - ${GREEN}已解決${NC}"
        else
            echo -e "${RED}$id${NC} (行: $line_num) - ${RED}未解決${NC}"
        fi
        echo -e "  ${YELLOW}描述:${NC} $(echo "$content" | sed 's/.*|//' | head -1 | cut -d'|' -f1 | xargs)"
        echo ""
    fi
}

# 顯示未解決錯誤
show_unresolved_errors() {
    echo -e "${CYAN}=== 未解決錯誤 ===${NC}"
    
    local count=0
    grep -n "狀態.*unresolved" "$MEMORY_FILE" | while read -r line; do
        local line_num=$(echo "$line" | cut -d: -f1)
        local content=$(echo "$line" | cut -d: -f2-)
        local id=$(echo "$content" | grep -o "\[E[0-9]\{3\}\]")
        
        echo -e "${RED}$id${NC} (行: $line_num)"
        echo -e "  ${YELLOW}描述:${NC} $(echo "$content" | grep -o "描述.*|" | sed 's/描述.*|//' | xargs)"
        echo -e "  ${BLUE}情境:${NC} $(echo "$content" | grep -o "情境.*|" | sed 's/情境.*|//' | xargs)"
        echo ""
        count=$((count + 1))
    done
    
    if [ "$count" -eq 0 ]; then
        echo -e "${GREEN}沒有未解決的錯誤！${NC}"
    else
        echo -e "${RED}總共有 $count 個未解決錯誤${NC}"
    fi
}

# 顯示最近學習
show_recent_learnings() {
    local limit="${1:-10}"
    
    echo -e "${CYAN}=== 最近 $limit 個學習 ===${NC}"
    
    # 取得所有學習和錯誤行
    grep -n "\[L[0-9]\{3\}\]\|\[E[0-9]\{3\}\]" "$MEMORY_FILE" | tail -"$limit" | while read -r line; do
        format_learning_line "$line"
    done
}

# 主程式
main() {
    # 檢查記憶檔案是否存在
    if [ ! -f "$MEMORY_FILE" ]; then
        echo -e "${RED}錯誤: 找不到記憶檔案 $MEMORY_FILE${NC}"
        exit 1
    fi
    
    # 解析參數
    local query=""
    local category=""
    local source=""
    local tag=""
    local show_errors=false
    local show_stats=false
    local recent_limit=""
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -c|--category)
                category="$2"
                shift 2
                ;;
            -s|--source)
                source="$2"
                shift 2
                ;;
            -t|--tag)
                tag="$2"
                shift 2
                ;;
            -e|--errors)
                show_errors=true
                shift
                ;;
            -r|--recent)
                if [[ $2 =~ ^[0-9]+$ ]]; then
                    recent_limit="$2"
                    shift 2
                else
                    recent_limit="10"
                    shift
                fi
                ;;
            -S|--stats)
                show_stats=true
                shift
                ;;
            -*)
                echo -e "${RED}錯誤: 未知選項 $1${NC}"
                show_help
                exit 1
                ;;
            *)
                query="$1"
                shift
                ;;
        esac
    done
    
    # 執行對應功能
    if [ "$show_stats" = true ]; then
        show_stats
    elif [ "$show_errors" = true ]; then
        show_unresolved_errors
    elif [ -n "$recent_limit" ]; then
        show_recent_learnings "$recent_limit"
    else
        search_learnings "$query" "$category" "$source" "$tag"
    fi
}

# 執行主程式
main "$@"