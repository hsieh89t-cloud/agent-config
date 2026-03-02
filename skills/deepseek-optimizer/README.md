# OpenClaw DeepSeek 優化專家技能

專門處理OpenClaw生態、DeepSeek API、提示詞工程、Agent工作流設計與成本優化相關任務的技能。

## 🎯 技能特色

### 1. **專業領域聚焦**
- 僅處理OpenClaw、DeepSeek、提示詞工程相關任務
- 非相關需求自動婉拒，避免能力漂移

### 2. **智能成本管控**
- DeepSeek模型智能選擇（chat/reasoner）
- Token消耗優化（V3.2節省58% token）
- 推理評分系統，動態調整輸出

### 3. **雙模式執行**
- **優化模式**：現有提示詞/流程優化
- **生成模式**：從0→1創建Agent任務

### 4. **生產就緒**
- RTCKD v5.3完全兼容
- OpenClaw官方工具規範對接
- 可直接部署的XML提示詞

## 📁 文件結構

```
deepseek-optimizer/
├── SKILL.md                    # 技能定義文件
├── README.md                   # 說明文件
├── install.sh                  # 安裝腳本
└── prompts/                    # 提示詞文件
    ├── openclaw_deepseek_optimizer_v3.2.xml          # V3.2優化版（推薦）
    ├── openclaw_deepseek_optimizer_lite_v3.1.xml     # V3.1精簡版
    └── openclaw_deepseek_optimizer_v3.0_full.md      # V3.0完整版
```

## 🚀 安裝方法

### 方法1：使用安裝腳本（推薦）
```bash
cd /path/to/deepseek-optimizer
sudo ./install.sh
```

### 方法2：手動安裝
```bash
# 複製到OpenClaw技能目錄
sudo cp -r deepseek-optimizer /usr/local/nvm/versions/node/v24.13.1/lib/node_modules/openclaw/skills/

# 重啟OpenClaw Gateway
openclaw gateway restart
```

## 🔧 配置要求

### 1. DeepSeek API金鑰
```bash
# 獲取API金鑰：https://platform.deepseek.com/api_keys
openclaw config set deepseek.apiKey YOUR_API_KEY
```

### 2. 設置默認模型
```bash
openclaw config set agents.defaults.model deepseek/deepseek-chat
```

### 3. Web工具配置（可選）
```json
{
  "tools": {
    "web": {
      "search": {
        "enabled": true,
        "provider": "brave",
        "maxResults": 5,
        "cacheTtlMinutes": 15
      }
    }
  }
}
```

## 📊 版本比較

| 版本 | Token消耗 | 特點 | 適用場景 |
|------|-----------|------|----------|
| **V3.2優化版** | ~500 tokens | 完整功能 + 智能成本管控 + 推理評分系統 | 生產環境，需要完整功能 |
| **V3.1精簡版** | ~300 tokens | 極簡設計，快速部署 | 測試環境，追求最低token消耗 |
| **V3.0完整版** | ~1200 tokens | 完整說明文檔 + Obsidian兼容 | 開發維護，需要詳細文檔 |

## 🧠 推理評分系統

### 評分邏輯
- **+3分**：多步邏輯、架構設計、數學計算
- **+2分**：模糊問題、策略規劃、風險評估
- **+1分**：新問題、高風險操作、複雜優化
- **-2分**：例行任務、單一答案查詢
- **-3分**：簡單查詢、格式轉換、確認類

### 輸出標記
- **≤5分**：快速回答，無標記
- **6-7分**：推理 + 🧠標記
- **≥8分**：深度推理 + 🧠🔥標記

## 🛠️ 使用示例

### 示例1：優化現有提示詞
```
切到優化模式，幫我把這份「每日產業情報監控」提示詞拆成主控+規格檔，目標每次執行減少至少30% token
```

### 示例2：生成新Agent任務
```
切到生成模式，幫我設計一個OpenClaw Brave API用量監控Agent，每日執行1次，超過門檻發Telegram告警
```

### 示例3：成本診斷
```
分析當前DeepSeek API使用情況，提供成本優化建議，輸出控制在400字以內
```

## 📈 預期效益

- **成本降低**：單次任務執行成本平均降低≥40%
- **效率提升**：部署與維護效率提升≥70%
- **質量提升**：提示詞結構更清晰，可維護性更好
- **穩定性**：抗干擾能力與長對話穩定性顯著提升

## 🔗 相關資源

- [OpenClaw官方文檔](https://docs.openclaw.ai)
- [DeepSeek API文檔](https://api-docs.deepseek.com)
- [RTCKD系統規範](https://github.com/rtckd/rtckd-system)
- [技能開發指南](https://docs.openclaw.ai/guides/skills)

## 🐛 問題回報

如遇問題，請提交至：
- GitHub Issues: [openclaw/openclaw](https://github.com/openclaw/openclaw/issues)
- Discord社群: [OpenClaw Discord](https://discord.com/invite/clawd)

## 📄 授權協議

本技能採用MIT授權協議。

---

**OpenClaw DeepSeek優化專家技能 - 讓您的Agent工作流更智能、更經濟！** 🚀