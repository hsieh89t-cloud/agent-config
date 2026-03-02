# 🔒 OpenClaw 安全配置指南

## 🚨 緊急安全事件處理

### 已發現的安全問題
**時間**：2026-03-02 05:40 UTC  
**問題**：Telegram Bot API金鑰意外提交到git工作目錄  
**金鑰**：`[已撤銷]`（原金鑰格式：10位數字:35位字符）  
**狀態**：已從工作目錄刪除，需要撤銷並重新生成

### 立即行動步驟
1. **撤銷洩漏的金鑰**：
   ```bash
   # 登入 Telegram @BotFather
   # 選擇您的bot
   # 選擇「Revoke current token」
   # 獲取新的API金鑰
   ```

2. **配置新的金鑰**：
   ```bash
   # 使用store_key.py安全儲存新金鑰
   cd /home/hsieh89t/.openclaw/workspace
   python3 store_key.py
   # 輸入名稱：@ysga168bot
   # 輸入新的Telegram Bot API金鑰
   ```

## 📁 安全文件結構

### 推薦的目錄結構
```
.openclaw/workspace/
├── config/
│   ├── .gitignore          # 排除敏感文件
│   ├── keys/               # ⚠️ 金鑰目錄（已排除）
│   │   └── secure_keys.json # API金鑰
│   └── scripts/            # 安全腳本
├── scripts/                # 公開腳本
└── skills/                 # 技能文件
```

### .gitignore 配置
```gitignore
# config/.gitignore
# 金鑰與敏感文件
keys/
*.key
*.pem
*.p12
*token*
*secret*
credentials*
.env
.env.local
.env.*.local

# 運行時文件
logs/
tmp/
cache/
*.log
memory/
HEARTBEAT.md
```

## 🔐 API金鑰安全管理

### 安全儲存原則
1. **永不硬編碼**：金鑰永遠不寫死在程式碼中
2. **環境變數優先**：使用環境變數或外部配置文件
3. **git排除**：所有金鑰文件必須在.gitignore中
4. **權限限制**：金鑰文件設置為600權限

### 安全儲存示例
```python
# ❌ 錯誤：硬編碼金鑰
TELEGRAM_TOKEN = "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"

# ✅ 正確：從外部文件讀取
import json
from pathlib import Path

KEY_FILE = Path.home() / ".openclaw" / "keys" / "telegram.json"
with open(KEY_FILE) as f:
    config = json.load(f)
TELEGRAM_TOKEN = config["token"]
```

### store_key.py 使用指南
```bash
# 安全儲存新金鑰
python3 store_key.py

# 互動式輸入：
# 1. 輸入金鑰名稱（如：deepseek_api）
# 2. 輸入API金鑰（隱藏輸入）
# 3. 確認金鑰
# 4. 添加備註（可選）
```

## 🛡️ Git安全最佳實踐

### 提交前檢查
```bash
# 檢查是否有敏感文件
git status

# 檢查.gitignore是否有效
git check-ignore -v path/to/file

# 檢查提交內容
git diff --cached
```

### 安全提交腳本
```bash
#!/bin/bash
# safe_commit.sh

# 檢查敏感文件
SENSITIVE_FILES=$(git ls-files | grep -E "\.(key|pem|p12|env)$|secret|token|password")
if [ -n "$SENSITIVE_FILES" ]; then
    echo "❌ 發現敏感文件："
    echo "$SENSITIVE_FILES"
    exit 1
fi

# 執行提交
git commit -m "$1"
```

### 萬一提交了敏感資訊
```bash
# 1. 立即撤銷提交
git reset --soft HEAD~1

# 2. 從歷史中移除文件
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch path/to/sensitive/file" \
  --prune-empty --tag-name-filter cat -- --all

# 3. 強制推送到遠端
git push origin --force --all

# 4. 立即撤銷洩漏的金鑰
```

## 🔧 安全工具配置

### OpenClaw配置安全
```json
{
  "deepseek": {
    "apiKey": "${DEEPSEEK_API_KEY}"  // 使用環境變數
  },
  "tools": {
    "web": {
      "search": {
        "provider": "brave",
        "apiKey": "${BRAVE_API_KEY}"  // 使用環境變數
      }
    }
  }
}
```

### 環境變數管理
```bash
# 設置環境變數
export DEEPSEEK_API_KEY="your-key-here"
export BRAVE_API_KEY="your-key-here"

# 使用.env文件（已排除在git外）
echo "DEEPSEEK_API_KEY=your-key-here" >> .env
echo "BRAVE_API_KEY=your-key-here" >> .env
```

## 📊 安全檢查清單

### 每日檢查
- [ ] 確認.gitignore包含所有敏感目錄
- [ ] 檢查git狀態是否有意外文件
- [ ] 驗證金鑰文件權限（應為600）

### 每周檢查
- [ ] 審查API金鑰使用情況
- [ ] 更新過期的金鑰
- [ ] 檢查git歷史是否有敏感資訊

### 每月檢查
- [ ] 輪換重要金鑰
- [ ] 審查安全日誌
- [ ] 更新安全配置

## 🚀 安全部署流程

### 開發環境
1. 使用測試金鑰
2. 金鑰存儲在本地`.env`文件
3. `.env`文件在.gitignore中

### 生產環境
1. 使用環境變數或密鑰管理服務
2. 不同環境使用不同金鑰
3. 定期輪換金鑰

### 備份與恢復
```bash
# 備份金鑰文件
cp -r config/keys/ keys_backup_$(date +%Y%m%d)/

# 恢復金鑰文件
cp -r keys_backup/config/keys/ config/
chmod 600 config/keys/*.json
```

## 📞 緊急聯絡

### 金鑰洩漏處理流程
1. **立即行動**：
   - 撤銷洩漏的金鑰
   - 從git歷史中移除敏感文件
   - 通知相關服務提供商

2. **調查原因**：
   - 檢查.gitignore配置
   - 審查提交流程
   - 更新安全策略

3. **預防措施**：
   - 加強提交前檢查
   - 設置git hooks
   - 定期安全培訓

### 聯絡資訊
- **GitHub倉庫**：立即設置security alerts
- **API提供商**：報告金鑰洩漏
- **安全團隊**：內部通報

---

## ✅ 安全狀態檢查

最後檢查時間：2026-03-02 05:45 UTC

### 當前狀態
- [x] 洩漏的金鑰文件已從工作目錄刪除
- [ ] Telegram Bot金鑰已撤銷（需手動執行）
- [x] .gitignore配置正確
- [x] 安全指南已創建
- [ ] 新金鑰已安全儲存（需手動執行）

### 待辦事項
1. [ ] 撤銷並重新生成Telegram Bot API金鑰
2. [ ] 使用store_key.py安全儲存新金鑰
3. [ ] 測試所有依賴金鑰的服務
4. [ ] 設置git pre-commit hook防止再次發生

---

**安全第一，預防為主！定期檢查，及時更新。** 🔒