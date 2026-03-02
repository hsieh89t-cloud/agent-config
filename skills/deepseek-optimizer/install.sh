#!/bin/bash
# OpenClaw DeepSeek優化專家技能安裝腳本

set -e

echo "🧠 安裝 OpenClaw DeepSeek 優化專家技能..."

# 檢查OpenClaw技能目錄
OPENCLAW_SKILLS_DIR="/usr/local/nvm/versions/node/v24.13.1/lib/node_modules/openclaw/skills"
if [ ! -d "$OPENCLAW_SKILLS_DIR" ]; then
    echo "❌ 找不到OpenClaw技能目錄: $OPENCLAW_SKILLS_DIR"
    echo "請確認OpenClaw已正確安裝"
    exit 1
fi

# 創建技能目錄
SKILL_DIR="$OPENCLAW_SKILLS_DIR/deepseek-optimizer"
echo "📁 創建技能目錄: $SKILL_DIR"
sudo mkdir -p "$SKILL_DIR"

# 複製技能文件
echo "📄 複製技能文件..."
sudo cp -r "$(dirname "$0")"/* "$SKILL_DIR/" 2>/dev/null || true

# 設置權限
echo "🔒 設置文件權限..."
sudo chmod -R 755 "$SKILL_DIR"

# 驗證安裝
if [ -f "$SKILL_DIR/SKILL.md" ]; then
    echo "✅ OpenClaw DeepSeek優化專家技能安裝完成！"
    echo ""
    echo "📋 技能資訊："
    echo "   名稱: deepseek-optimizer"
    echo "   描述: OpenClaw+DeepSeek優化專家，專門處理OpenClaw生態、DeepSeek API、提示詞工程相關任務"
    echo "   Emoji: 🧠"
    echo ""
    echo "🚀 使用方法："
    echo "   1. 重啟OpenClaw Gateway: openclaw gateway restart"
    echo "   2. 技能將自動出現在可用技能列表中"
    echo "   3. 當任務涉及OpenClaw、DeepSeek、提示詞優化時，系統會自動使用此技能"
    echo ""
    echo "📁 內置提示詞版本："
    echo "   - V3.2優化版 (~500 tokens): prompts/openclaw_deepseek_optimizer_v3.2.xml"
    echo "   - V3.1精簡版 (~300 tokens): prompts/openclaw_deepseek_optimizer_lite_v3.1.xml"
    echo "   - V3.0完整版 (~1200 tokens): prompts/openclaw_deepseek_optimizer_v3.0_full.md"
else
    echo "❌ 安裝失敗，SKILL.md文件未找到"
    exit 1
fi