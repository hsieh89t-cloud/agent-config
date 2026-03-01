# OpenClaw Web Tools Specification
> **臨時版本** - 基於OpenClaw 2026.2官方文檔摘要
> **注意**：完整規範請參考 docs.openclaw.ai

## 概述
OpenClaw Web工具提供網絡搜索與內容獲取能力，是Agent與外部信息源交互的核心接口。

## 核心工具

### web_search
**功能**：通過Brave Search API執行網絡搜索

**參數規範**：
```json
{
  "query": "搜索關鍵詞（字符串，必需）",
  "count": "結果數量（1-10，可選）",
  "country": "國家代碼（如'US'，可選）",
  "freshness": "時間過濾（如'pd'、'pw'，可選）"
}
```

**使用限制**：
- 每月請求次數限制取決於Brave API訂閱等級
- 免費版通常有基本請求配額
- 必須配置有效的BRAVE_API_KEY

**錯誤處理**：
- `missing_brave_api_key`：API密鑰未配置
- `rate_limit_exceeded`：請求頻率超限
- `invalid_query`：查詢參數無效

### web_fetch
**功能**：獲取網頁內容並提取可讀文本

**參數規範**：
```json
{
  "url": "目標URL（必需）",
  "extractMode": "提取模式（'markdown'或'text'）",
  "maxChars": "最大字符數（可選）"
}
```

**使用限制**：
- 僅支持公開可訪問的網頁
- 不支援需要登錄或付費牆的內容
- 遵守robots.txt協議

## 成本管控規則

### 搜索優化
1. **查詢合併**：相似查詢應合併執行
2. **結果緩存**：相同查詢結果應緩存24小時
3. **頻率控制**：避免短時間內密集請求

### 錯誤重試
1. **瞬時錯誤**：立即重試1次
2. **限額錯誤**：等待1小時後重試
3. **配置錯誤**：停止並報告需要人工干預

## 兼容性要求

### OpenClaw Agent集成
- 所有工具調用必須通過OpenClaw Gateway
- 必須遵守工具權限白名單
- 必須實現標準錯誤處理接口

### 安全規範
- 禁止繞過API密鑰驗證
- 禁止訪問惡意或非法網站
- 禁止洩露用戶隱私信息

## 部署配置

### 環境變數
```bash
BRAVE_API_KEY=your_brave_api_key_here
```

### 驗證測試
```bash
# 測試API密鑰有效性
openclaw web search --query "test" --count 1
```

---

**版本**：2026.2.0-temp  
**最後更新**：2026-03-01  
**狀態**：臨時規範，待替換為官方文檔