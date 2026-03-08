#!/bin/bash
# 學習記錄腳本 - 基於 Adaptive Learning Agent 設計理念

MEMORY_FILE="$HOME/.openclaw/workspace/MEMORY.md"
LEARNING_TEMPLATE="$HOME/.openclaw/workspace/scripts/learning/templates"

# 顏色定義
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 建立模板目錄
mkdir -p "$LEARNING_TEMPLATE"

# 顯示使用說明
show_help() {
    echo -e "${CYAN}學習記錄系統 - 基於 Adaptive Learning Agent 設計理念${NC}"
    echo "用法: $0 [類型] [選項]"
    echo ""
    echo "類型:"
    echo "  learning    記錄成功學習"
    echo "  error       記錄錯誤與解決方案"
    echo "  fact        記錄事實"
    echo "  experience  記錄經驗學習"
    echo ""
    echo "選項:"
    echo "  -h, --help           顯示此說明"
    echo "  -i, --interactive    互動模式"
    echo "  --template NAME      使用模板"
    echo ""
    echo "範例:"
    echo "  $0 learning --interactive"
    echo "  $0 error --template api-error"
}

# 產生學習 ID
generate_learning_id() {
    local prefix="$1"
    local last_id=$(grep -o "\[${prefix}[0-9]\{3\}\]" "$MEMORY_FILE" | tail -1 | grep -o "[0-9]\{3\}" || echo "0")
    local next_id=$((last_id + 1))
    printf "[%s%03d]" "$prefix" "$next_id"
}

# 取得當前日期
get_current_date() {
    date +"%Y-%m-%d"
}

# 互動模式記錄學習
interactive_learning() {
    echo -e "${CYAN}=== 記錄成功學習 ===${NC}"
    
    # 學習內容
    echo -e "${YELLOW}學習內容 (什麼被學到了？):${NC}"
    read -r content
    if [ -z "$content" ]; then
        echo -e "${RED}錯誤: 學習內容不能為空${NC}"
        return 1
    fi
    
    # 選擇類別
    echo -e "${YELLOW}選擇類別:${NC}"
    echo "  1) technique - 技術方法"
    echo "  2) bug-fix - 錯誤修復"
    echo "  3) best-practice - 最佳實踐"
    echo "  4) constraint - 限制條件"
    echo "  5) api-quirk - API 特性"
    echo "  6) error-handling - 錯誤處理"
    echo "  7) optimization - 效能優化"
    echo "  8) security - 安全考量"
    echo "  9) 其他 (請輸入)"
    
    read -r category_choice
    case $category_choice in
        1) category="technique" ;;
        2) category="bug-fix" ;;
        3) category="best-practice" ;;
        4) category="constraint" ;;
        5) category="api-quirk" ;;
        6) category="error-handling" ;;
        7) category="optimization" ;;
        8) category="security" ;;
        *) 
            echo -e "${YELLOW}請輸入類別名稱:${NC}"
            read -r category
            ;;
    esac
    
    # 選擇來源
    echo -e "${YELLOW}選擇來源:${NC}"
    echo "  1) user-correction - 使用者修正"
    echo "  2) error-discovery - 錯誤發現"
    echo "  3) successful-pattern - 成功模式"
    echo "  4) user-feedback - 使用者回饋"
    echo "  5) system-observation - 系統觀察"
    echo "  6) experimentation - 實驗結果"
    echo "  7) 其他 (請輸入)"
    
    read -r source_choice
    case $source_choice in
        1) source="user-correction" ;;
        2) source="error-discovery" ;;
        3) source="successful-pattern" ;;
        4) source="user-feedback" ;;
        5) source="system-observation" ;;
        6) source="experimentation" ;;
        *) 
            echo -e "${YELLOW}請輸入來源名稱:${NC}"
            read -r source
            ;;
    esac
    
    # 上下文
    echo -e "${YELLOW}上下文 (可選，這個學習適用的情境):${NC}"
    read -r context
    
    # 標籤
    echo -e "${YELLOW}標籤 (可選，用逗號分隔):${NC}"
    read -r tags
    
    # 產生學習記錄
    local learning_id=$(generate_learning_id "L")
    local current_date=$(get_current_date)
    
    local learning_record="\n- $learning_id $content | 類別: $category | 來源: $source | 日期: $current_date"
    
    if [ -n "$context" ]; then
        learning_record="$learning_record | 上下文: $context"
    fi
    
    if [ -n "$tags" ]; then
        learning_record="$learning_record | 標籤: $tags"
    fi
    
    # 確認
    echo -e "\n${CYAN}=== 學習記錄預覽 ===${NC}"
    echo -e "$learning_record"
    echo -e "\n${YELLOW}確認記錄？ (y/n):${NC}"
    read -r confirm
    
    if [[ "$confirm" =~ ^[Yy]$ ]]; then
        # 找到 structured_memory_framework 區塊
        if grep -q "## structured_memory_framework" "$MEMORY_FILE"; then
            # 在框架內添加學習記錄
            sed -i "/## structured_memory_framework/a\\$learning_record" "$MEMORY_FILE"
            echo -e "${GREEN}學習記錄已添加！${NC}"
            echo -e "學習 ID: $learning_id"
        else
            echo -e "${RED}錯誤: 找不到 structured_memory_framework 區塊${NC}"
            return 1
        fi
    else
        echo -e "${YELLOW}取消記錄${NC}"
    fi
}

# 互動模式記錄錯誤
interactive_error() {
    echo -e "${CYAN}=== 記錄錯誤與解決方案 ===${NC}"
    
    # 錯誤描述
    echo -e "${YELLOW}錯誤描述 (什麼出錯了？):${NC}"
    read -r error_description
    if [ -z "$error_description" ]; then
        echo -e "${RED}錯誤: 錯誤描述不能為空${NC}"
        return 1
    fi
    
    # 情境
    echo -e "${YELLOW}情境 (在做什麼時發生錯誤？):${NC}"
    read -r context
    if [ -z "$context" ]; then
        echo -e "${RED}錯誤: 情境不能為空${NC}"
        return 1
    fi
    
    # 解決方案
    echo -e "${YELLOW}解決方案 (如何修復？，如果還不知道可留空):${NC}"
    read -r solution
    
    # 預防提示
    echo -e "${YELLOW}預防提示 (如何避免再次發生？，可選):${NC}"
    read -r prevention_tip
    
    # 狀態
    local status="unresolved"
    if [ -n "$solution" ]; then
        status="resolved"
        echo -e "${GREEN}錯誤標記為已解決${NC}"
    else
        echo -e "${YELLOW}錯誤標記為未解決${NC}"
    fi
    
    # 產生錯誤記錄
    local error_id=$(generate_learning_id "E")
    local current_date=$(get_current_date)
    
    local error_record="\n- $error_id $error_description | 情境: $context | 狀態: $status | 日期: $current_date"
    
    if [ -n "$solution" ]; then
        error_record="$error_record | 解決方案: $solution"
    fi
    
    if [ -n "$prevention_tip" ]; then
        error_record="$error_record | 預防提示: $prevention_tip"
    fi
    
    # 確認
    echo -e "\n${CYAN}=== 錯誤記錄預覽 ===${NC}"
    echo -e "$error_record"
    echo -e "\n${YELLOW}確認記錄？ (y/n):${NC}"
    read -r confirm
    
    if [[ "$confirm" =~ ^[Yy]$ ]]; then
        # 找到 structured_memory_framework 區塊
        if grep -q "## structured_memory_framework" "$MEMORY_FILE"; then
            # 在框架內添加錯誤記錄
            sed -i "/## structured_memory_framework/a\\$error_record" "$MEMORY_FILE"
            echo -e "${GREEN}錯誤記錄已添加！${NC}"
            echo -e "錯誤 ID: $error_id"
            echo -e "狀態: $status"
        else
            echo -e "${RED}錯誤: 找不到 structured_memory_framework 區塊${NC}"
            return 1
        fi
    else
        echo -e "${YELLOW}取消記錄${NC}"
    fi
}

# 建立模板
create_template() {
    local template_name="$1"
    
    case $template_name in
        "api-error")
            cat > "$LEARNING_TEMPLATE/api-error.txt" << 'EOF'
# API 錯誤模板

## 錯誤描述
[描述 API 錯誤]

## 情境
[使用什麼 API、執行什麼操作時發生]

## 錯誤訊息
[完整的錯誤訊息]

## 根本原因
[造成錯誤的根本原因]

## 解決方案
[如何修復錯誤]

## 預防措施
[如何避免再次發生]

## 相關資源
[相關文件、Issue、討論連結]

## 測試方法
[如何測試修復是否有效]

## 影響範圍
[這個錯誤影響哪些功能]
EOF
            echo -e "${GREEN}API 錯誤模板已建立${NC}"
            ;;
        "best-practice")
            cat > "$LEARNING_TEMPLATE/best-practice.txt" << 'EOF'
# 最佳實踐模板

## 實踐名稱
[實踐的名稱]

## 適用情境
[在什麼情況下使用這個實踐]

## 具體做法
[詳細的實施步驟]

## 預期效益
[實施後預期得到的好處]

## 注意事項
[需要注意的細節或限制]

## 範例程式碼
[實際的程式碼範例]

## 相關模式
[相關的其他實踐或模式]

## 驗證方法
[如何驗證這個實踐的有效性]
EOF
            echo -e "${GREEN}最佳實踐模板已建立${NC}"
            ;;
        "bug-fix")
            cat > "$LEARNING_TEMPLATE/bug-fix.txt" << 'EOF'
# 錯誤修復模板

## 錯誤現象
[觀察到的錯誤現象]

## 重現步驟
[如何重現這個錯誤]

## 預期行為
[正確的行為應該是什麼]

## 實際行為
[實際發生的錯誤行為]

## 根本原因分析
[造成錯誤的根本原因]

## 修復方案
[具體的修復方法]

## 測試方法
[如何測試修復是否有效]

## 影響評估
[修復對系統的影響]

## 預防措施
[如何預防類似錯誤]
EOF
            echo -e "${GREEN}錯誤修復模板已建立${NC}"
            ;;
        *)
            echo -e "${RED}錯誤: 未知模板 '$template_name'${NC}"
            echo -e "${YELLOW}可用模板: api-error, best-practice, bug-fix${NC}"
            return 1
            ;;
    esac
}

# 主程式
main() {
    # 檢查記憶檔案是否存在
    if [ ! -f "$MEMORY_FILE" ]; then
        echo -e "${RED}錯誤: 找不到記憶檔案 $MEMORY_FILE${NC}"
        exit 1
    fi
    
    # 解析參數
    local record_type=""
    local interactive=false
    local template_name=""
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -i|--interactive)
                interactive=true
                shift
                ;;
            --template)
                template_name="$2"
                shift 2
                ;;
            -*)
                echo -e "${RED}錯誤: 未知選項 $1${NC}"
                show_help
                exit 1
                ;;
            *)
                if [ -z "$record_type" ]; then
                    record_type="$1"
                else
                    echo -e "${RED}錯誤: 未知參數 $1${NC}"
                    show_help
                    exit 1
                fi
                shift
                ;;
        esac
    done
    
    # 處理模板建立
    if [ -n "$template_name" ]; then
        create_template "$template_name"
        exit 0
    fi
    
    # 執行對應功能
    case $record_type in
        "learning")
            if [ "$interactive" = true ]; then
                interactive_learning
            else
                echo -e "${RED}錯誤: 學習記錄需要互動模式${NC}"
                show_help
                exit 1
            fi
            ;;
        "error")
            if [ "$interactive" = true ]; then
                interactive_error
            else
                echo -e "${RED}錯誤: 錯誤記錄需要互動模式${NC}"
                show_help
                exit 1
            fi
            ;;
        "fact"|"experience")
            echo -e "${YELLOW}功能開發中...${NC}"
            echo -e "請先使用 learning 或 error 類型"
            ;;
        "")
            echo -e "${RED}錯誤: 請指定記錄類型${NC}"
            show_help
            exit 1
            ;;
        *)
            echo -e "${RED}錯誤: 未知記錄類型 '$record_type'${NC}"
            show_help
            exit 1
            ;;
    esac
}

# 執行主程式
main "$@"