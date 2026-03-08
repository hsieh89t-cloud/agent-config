# 技能索引 (Skills Index)

基於 Capability Awareness System 設計理念建立的技能發現與管理系統。

## 設計原則

1. **技能優先 (Skills-First)**：代理需要知道可用技能
2. **按需載入 (On-Demand)**：需要時才讀取完整文件
3. **零開銷 (Zero Overhead)**：不使用時不佔用資源

## 可用技能清單

### 學術研究 (academic-research)
- **位置**：`skills/academic-research/`
- **安裝日期**：2026-03-08
- **用途**：搜尋學術論文、進行文獻回顧
- **何時使用**：
  - 需要找特定主題的研究論文
  - 進行文獻綜述或研究現狀分析
  - 查找作者或特定論文的引用鏈
- **核心指令**：
  ```bash
  # 主題搜尋
  python3 scripts/scholar-search.py search "主題" --limit 10
  
  # 文獻回顧
  python3 scripts/literature-review.py "研究主題" --papers 20 --output review.md
  ```
- **風險等級**：低（僅讀取公開 API）

### 上下文衛生 (context-hygiene)
- **位置**：`skills/context-hygiene/`
- **用途**：上下文維護與優化協議
- **何時使用**：
  - 會話過長需要壓縮上下文時
  - 定期上下文維護
  - 優化 token 使用效率
- **觸發方式**：自動或手動執行

### 代理配置 (agent-config)
- **位置**：`skills/agent-config/`
- **用途**：修改核心上下文檔案
- **何時使用**：
  - 需要調整代理行為、規則、個性時
  - 更新操作流程或安全規則
  - 修改記憶架構或委派模式

### 腦力激盪 (brainstorming)
- **位置**：`skills/brainstorming/`
- **用途**：創意工作前的設計與規劃
- **何時使用**：**任何創意工作前必須使用**
  - 創建新功能或組件
  - 系統設計與架構規劃
  - 新增功能或修改行為

### 瀏覽器自動化 (agent-browser)
- **位置**：`skills/agent-browser/`
- **用途**：無頭瀏覽器自動化
- **何時使用**：
  - 需要網頁爬取或自動化時
  - 互動式網頁操作
  - 網頁快照與分析

## 技能使用流程

### 1. 技能發現
代理在每個會話開始時：
1. 掃描 `skills/` 目錄
2. 讀取本索引檔案了解可用技能
3. 建立技能心智模型

### 2. 技能選擇
當任務出現時：
1. 匹配任務類型與技能用途
2. 參考「何時使用」指引
3. 選擇最合適的技能

### 3. 技能執行
1. 讀取對應的 SKILL.md
2. 按照技能指引執行
3. 記錄技能使用情況

## 技能安裝記錄

### 2026-03-08
- ✅ **academic-research**：學術研究技能（已安裝）
- ❌ **active-maintenance**：系統維護技能（不安裝，風險考量）
- 📚 **capability-awareness**：技能發現系統（學習模式）

### 評估不通過的技能
- **active-maintenance**：自動刪除功能風險過高
- **capability-awareness**：功能與現有系統重疊，採學習模式

## 技能開發指引

### 新技能要求
1. **明確的 SKILL.md**：包含用途、何時使用、指令範例
2. **風險評估**：在安裝前進行安全性評估
3. **記憶記錄**：安裝後記錄至記憶中樞

### 技能審查
- **每月一次**：檢查所有技能狀態
- **安全性審查**：評估技能風險變化
- **使用統計**：記錄技能使用頻率

## 參考資料

- **Capability Awareness System**：https://github.com/pfaria32/openclaw-capability-awareness
- **設計理念**：Skills-First, On-Demand Loading, Zero Overhead
- **應用模式**：技能卡 + 完整文件的兩層結構

---
*最後更新：2026-03-08 | 基於 Capability Awareness System 設計理念*