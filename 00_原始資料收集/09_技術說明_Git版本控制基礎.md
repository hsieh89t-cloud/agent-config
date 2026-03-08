---
title: Git版本控制基礎教學
source: /home/ysga/文件/技術文檔/git-guide.md
collected_at: 2026-03-08 16:40
status: 原始資料
data_type: Markdown文件
---

# Git版本控制基礎教學

Git是一個分散式版本控制系統，用於追蹤文件變更和協同開發。

## 基本概念

### 倉庫（Repository）
- 本地倉庫：本機上的版本庫
- 遠端倉庫：伺服器上的版本庫（如GitHub、GitLab）

### 三種狀態
1. **工作目錄**：實際文件
2. **暫存區**：準備提交的變更
3. **本地倉庫**：已提交的版本

## 常用指令

### 初始化與克隆
- git init：初始化新倉庫
- git clone <url>：克隆遠端倉庫

### 基本工作流
- git status：查看狀態
- git add <file>：添加到暫存區
- git commit -m "訊息"：提交變更
- git push：推送到遠端
- git pull：從遠端拉取

### 分支管理
- git branch：查看分支
- git branch <name>：創建分支
- git checkout <name>：切換分支
- git merge <name>：合併分支

### 查看歷史
- git log：查看提交歷史
- git diff：查看變更內容
- git show <commit>：查看特定提交

## 最佳實踐
1. 提交訊息清晰明確
2. 頻繁提交，每次提交一個邏輯單元
3. 使用分支進行功能開發
4. 定期與遠端同步
5. 解決衝突時仔細檢查