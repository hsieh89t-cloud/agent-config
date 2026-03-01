# DeepSeek API Specification
> **臨時版本** - 基於DeepSeek API官方文檔摘要
> **注意**：完整規範請參考 api-docs.deepseek.com

## 概述
DeepSeek API提供大語言模型推理服務，支持對話、推理、代碼生成等多種任務。

## 核心模型

### 可用模型
1. **deepseek-chat**
   - 用途：通用對話與任務處理
   - 上下文：128K tokens
   - 特點：平衡性能與成本

2. **deepseek-reasoner**
   - 用途：複雜推理與邏輯任務
   - 上下文：128K tokens
   - 特點：強化推理能力

### 模型選擇原則
- **日常任務**：優先使用deepseek-chat
- **複雜推理**：切換到deepseek-reasoner
- **成本敏感**：根據任務複雜度選擇

## API使用規範

### 請求格式
```json
{
  "model": "deepseek-chat",
  "messages": [
    {"role": "system", "content": "系統提示詞"},
    {"role": "user", "content": "用戶輸入"}
  ],
  "temperature": 0.7,
  "max_tokens": 2000
}
```

### 響應格式
```json
{
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "AI回應內容"
      }
    }
  ],
  "usage": {
    "prompt_tokens": 100,
    "completion_tokens": 150,
    "total_tokens": 250
  }
}
```

## 成本管控規則

### Token計算
1. **輸入tokens**：提示詞+上下文歷史
2. **輸出tokens**：AI生成內容
3. **總tokens**：輸入+輸出

### 成本優化策略
1. **提示詞精簡**：移除不必要的修飾語和重複內容
2. **上下文管理**：定期清理無關歷史
3. **輸出限制**：設置合理的max_tokens參數
4. **模型選擇**：根據任務需求選擇最經濟模型

### 免費額度
- DeepSeek API目前提供免費使用額度
- 具體限額請參考官方文檔
- 超出免費額度後可能產生費用

## 錯誤處理

### 常見錯誤碼
- `invalid_api_key`：API密鑰無效
- `rate_limit_exceeded`：請求頻率超限
- `insufficient_quota`：額度不足
- `model_not_found`：模型名稱錯誤

### 重試策略
1. **瞬時錯誤**：延遲1秒後重試，最多3次
2. **限額錯誤**：等待1分鐘後重試，最多2次
3. **配置錯誤**：停止並報告需要人工干預

## 兼容性要求

### OpenClaw集成
- 必須通過OpenClaw Gateway代理請求
- 必須實現標準的錯誤處理接口
- 必須支持模型動態切換

### 安全規範
- API密鑰必須安全存儲，禁止硬編碼
- 請求內容必須符合使用條款
- 禁止用於違法或有害用途

## 部署配置

### 環境變數
```bash
DEEPSEEK_API_KEY=your_deepseek_api_key_here
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
```

### 驗證測試
```bash
# 測試API密鑰有效性
curl https://api.deepseek.com/v1/chat/completions \
  -H "Authorization: Bearer $DEEPSEEK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"deepseek-chat","messages":[{"role":"user","content":"Hello"}]}'
```

---

**版本**：v1.0-temp  
**最後更新**：2026-03-01  
**狀態**：臨時規範，待替換為官方文檔