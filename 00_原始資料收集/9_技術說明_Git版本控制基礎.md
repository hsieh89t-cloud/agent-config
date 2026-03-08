---
title: 技術說明_Git版本控制基礎
source: 示例資料
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
重新初始化已存在的 Git 版本庫於 /home/ysga/.openclaw/workspace/.git/

### 基本工作流
位於分支 main
您的分支領先 'origin/main' 共 19 個提交。
  （使用 "git push" 來發布您的本機提交）

尚未暫存以備提交的變更：
  （使用 "git add <檔案>..." 更新要提交的內容）
  （使用 "git restore <檔案>..." 捨棄工作區的改動）
	修改：     AGENTS.md
	修改：     MEMORY.md
	修改：     SKILLS_INDEX.md
	修改：     TOOLS.md
	修改：     scripts/legal_batch_processor_v4.py
	修改：     skills/REGISTRY.md

未追蹤的檔案:
  （使用 "git add <檔案>..." 以包含要提交的內容）
	.clawhub/
	.openclaw/
	"00_\345\216\237\345\247\213\350\263\207\346\226\231\346\224\266\351\233\206/"
	"90_\346\250\241\346\235\277/"
	context-cleanup-audit.json
	scripts/__pycache__/
	scripts/layered_generation_v2.py
	scripts/legal_batch_processor_v3.1.py
	scripts/legal_batch_processor_v3.2.py
	scripts/legal_batch_processor_v3.py
	scripts/legal_batch_processor_v5.py
	scripts/quick_test.py
	scripts/setup_cron.sh
	scripts/test_batch_single.py
	scripts/test_chat_simple.py
	scripts/test_layered_simple.py
	scripts/test_prompt_variants.py
	scripts/test_v22_single.py
	scripts/validate_template_format.py
	"scripts/\346\263\225\345\276\213\346\242\235\346\226\207\347\265\220\346\247\213\345\214\226\346\224\271\351\200\262\346\274\224\347\244\272.py"
	"scripts/\346\263\225\345\276\213\346\242\235\346\226\207\347\265\220\346\247\213\345\214\226\347\224\237\346\210\220_v2.2_\345\237\267\350\241\214\350\205\263\346\234\254.py"
	"scripts/\346\270\254\350\251\246\345\237\267\350\241\214_v2.2.py"
	skills/agent-browser/
	skills/agent-config/
	skills/brainstorming/
	skills/context-clean-up/
	skills/context-hygiene/
	skills/openclaw-config/
	"\346\263\225\345\276\213\350\263\207\346\226\231\345\272\253\345\255\220\344\273\243\347\220\206\345\237\267\350\241\214\346\236\266\346\247\213_v1.md"
	"\347\254\254\344\272\214\345\244\247\350\205\246\350\263\207\346\226\231\345\272\253\350\210\207OpenClaw\344\273\243\347\220\206\345\267\245\344\275\234\345\215\200\346\236\266\346\247\213\350\250\255\350\250\210.md"

修改尚未加入提交（使用 "git add" 和/或 "git commit -a"）

### 分支管理
* main

### 查看歷史
commit 62fb9b36514d493f504a6ed131c1bb32d365bd16
Author: hsieh89t-cloud <hsieh89t@gmail.com>
Date:   Sat Mar 7 06:03:50 2026 +0800

    feat(batch): add rerun list generation with summary reporting

commit ae05d26abe90ec7ae00fe569fee02657d77e77ce
Author: hsieh89t-cloud <hsieh89t@gmail.com>
Date:   Sat Mar 7 05:55:05 2026 +0800

    fix(legal-batch): prevent fallback from copying statute text; mark needs_regen

commit 4f642b0e9a37cad1629175a41ede7d2aa5b602d3
Author: hsieh89t-cloud <hsieh89t@gmail.com>
Date:   Sat Mar 7 05:42:21 2026 +0800

    feat(legal-batch): enforce immutable statute text guard + switch to qwen 4k profile

commit 7d9388670fe377fa6800004fec3af4c86b2de0ee
Author: hsieh89t-cloud <hsieh89t@gmail.com>
Date:   Sat Mar 7 05:25:01 2026 +0800

    chore(local-llm): add qwen3.5 4k ctx modelfile preset

commit 3620a7b854fac1279884499abe86c359a711fe87
Author: hsieh89t-cloud <hsieh89t@gmail.com>
Date:   Sat Mar 7 02:01:40 2026 +0800

    chore(memory): enforce context-compression archival habit and strategy indexing

commit a383a2cec59ba340c8c338b4ec4705fc6978fe2a
Author: hsieh89t-cloud <hsieh89t@gmail.com>
Date:   Sat Mar 7 01:59:43 2026 +0800

    chore(memory): record dated rollback-log preference and Obsidian memory hub preference

commit 3a13a4b2a7fcde6aaa12f63ca73c5e3c92bd69bd
Author: hsieh89t-cloud <hsieh89t@gmail.com>
Date:   Fri Mar 6 23:56:13 2026 +0800

    新增模型路由規範：DeepSeek規劃 + Qwen3.5執行

commit efe0132b6ea64b82a413b0590e427edaf496ae0f
Author: hsieh89t-cloud <hsieh89t@gmail.com>
Date:   Fri Mar 6 17:37:47 2026 +0800

    feat(dashboard): add pause/resume and quit hotkeys

commit fc00a2141c86ed4bb74171e024ef3b903824ec46
Author: hsieh89t-cloud <hsieh89t@gmail.com>
Date:   Fri Mar 6 17:36:07 2026 +0800

    refactor(dashboard): switch to compact single-screen layout

commit 7e89856d17902f5ce87ff5b85ca1437156157a44
Author: hsieh89t-cloud <hsieh89t@gmail.com>
Date:   Fri Mar 6 17:33:51 2026 +0800

    chore(dashboard): remove OpenClaw recent log section for cleaner view

commit 51e916d2fa63cfca0abb02503456688d203a6ccb
Author: hsieh89t-cloud <hsieh89t@gmail.com>
Date:   Fri Mar 6 17:32:19 2026 +0800

    feat(dashboard): convert to full PC health overview dashboard

commit 993bb1b7bbe2bd90e1c45320ba09a1586f0f416b
Author: hsieh89t-cloud <hsieh89t@gmail.com>
Date:   Fri Mar 6 17:29:52 2026 +0800

    fix(dashboard): resolve crash by using ASCII shell variables

commit 2b227a82bf45379c856df779e8cb7aa1315b2754
Author: hsieh89t-cloud <hsieh89t@gmail.com>
Date:   Fri Mar 6 17:27:59 2026 +0800

    feat(dashboard): localize Traditional Chinese UI and add desktop shortcuts

commit 73661b91c09ebe6d4ced63304827cb119f838a63
Author: hsieh89t-cloud <hsieh89t@gmail.com>
Date:   Fri Mar 6 17:24:10 2026 +0800

    feat: add local system dashboard script for OpenClaw+Ollama monitoring

commit d1f96bf98d6311a07233948761bf782e25c80f83
Author: hsieh89t-cloud <hsieh89t@gmail.com>
Date:   Fri Mar 6 12:17:53 2026 +0800

    chore(memory): prioritize local execution and ROC statute summarization plan

commit affb2ae860037916ca5f9f12564145b44c57412a
Author: hsieh89t-cloud <hsieh89t@gmail.com>
Date:   Fri Mar 6 12:11:36 2026 +0800

    chore(memory): enforce sentinel+QC and no fabricated statutes

commit e7c47d3de544ec45e0b4f9f0f2f8c1d615edb5a7
Author: hsieh89t-cloud <hsieh89t@gmail.com>
Date:   Fri Mar 6 12:10:22 2026 +0800

    chore(memory): narrow legal scope to ROC law only

commit d17b1d5957a06fb33be1c899a31005645ccb24bc
Author: hsieh89t-cloud <hsieh89t@gmail.com>
Date:   Fri Mar 6 12:09:34 2026 +0800

    chore(memory): capture folder-architecture priority and cross-jurisdiction strategy

commit a617cb78621b8ccbed302df9ff7b8077f6d8bdcd
Author: hsieh89t-cloud <hsieh89t@gmail.com>
Date:   Fri Mar 6 12:07:14 2026 +0800

    chore(memory): record daily task cadence and DeepSeek preference for legal reasoning

commit 9f7b9748516189a360503181d0fb2877ff3e8c99
Author: hsieh89t-cloud <hsieh89t@gmail.com>
Date:   Fri Mar 6 09:44:04 2026 +0800

    Update long-term and daily memory summaries after legal AI setup

commit 9745a5702df1feec94528f5558f2bddcd13e99fb
Author: hsieh89t-cloud <hsieh89t@gmail.com>
Date:   Fri Mar 6 08:48:41 2026 +0800

    Add guard/task/memory safety policies and bootstrap guard layer

commit 9701ede34821f4cb79fd5c6517536939cec749be
Author: hsieh89t-cloud <hsieh89t@gmail.com>
Date:   Fri Mar 6 08:40:36 2026 +0800

    Add workspace guidance docs (AGENTS, SOUL, TOOLS)

commit 1bccf613105c7e5787d4014900ffb46a96e7fc42
Author: hsieh89t-cloud <hsieh89t@gmail.com>
Date:   Fri Mar 6 08:18:27 2026 +0800

    Initialize memory/state structures and adaptive reasoning skill

commit 9639e663fa335279280a930f6c946bb6925f0b3b
Author: 小育 <hsieh89t@gmail.com>
Date:   Thu Mar 5 17:52:53 2026 +0800

    auto backup 2026-03-05 17:52:53

commit ec9baa155c5bc3cb0abd2e1a7f5163eb37dd70bf
Author: 小育 <hsieh89t@gmail.com>
Date:   Thu Mar 5 17:44:24 2026 +0800

    auto backup 2026-03-05 17:44:24

commit 9a5a8bd5baa58001911e50089327e1e0c6eac324
Author: 小育 <hsieh89t@gmail.com>
Date:   Thu Mar 5 17:43:57 2026 +0800

    auto backup 2026-03-05 17:43:57

commit 0c3430ea1cc8562d79d9a0ac5bdf52835f58602e
Merge: d2c56ef 317708d
Author: 小育 <hsieh89t@gmail.com>
Date:   Thu Mar 5 17:42:11 2026 +0800

    Merge remote-tracking branch 'origin/main'

commit d2c56ef55132958895c91b072b5ed883ef8760fb
Author: 小育 <hsieh89t@gmail.com>
Date:   Thu Mar 5 17:41:45 2026 +0800

    backup agent config + skills

commit e966e4715fc9966ebe821764cc4aaa35ea821251
Author: 小育 <hsieh89t@gmail.com>
Date:   Thu Mar 5 17:39:49 2026 +0800

    backup agent config

commit 717a3abcfa15a986f3a9b67d723f94a8a8a69635
Author: 小育 <hsieh89t@gmail.com>
Date:   Thu Mar 5 17:34:57 2026 +0800

    Add pre-commit secret scan hook

commit ac8ac883e8228a8d0c8adc7ccebbc492590a7ff3
Author: 小育 <hsieh89t@gmail.com>
Date:   Thu Mar 5 17:34:17 2026 +0800

    Add agent config baseline (identity/user/state/memory/skills)

commit 33069dbd9ec85c65e79263f6f05336d269bedc66
Author: hsieh89t-cloud <hsieh89t@gmail.com>
Date:   Thu Mar 5 17:17:08 2026 +0800

    Delete USER.md

commit d72e88d95b66dd4b06b2b845b1f1d30781353bf1
Author: hsieh89t-cloud <hsieh89t@gmail.com>
Date:   Thu Mar 5 17:17:01 2026 +0800

    Delete IDENTITY.md

commit 2cc7c82510389a59f8578080717da4549a658a6b
Author: hsieh89t-cloud <hsieh89t@gmail.com>
Date:   Thu Mar 5 17:16:53 2026 +0800

    Delete .gitignore

commit 24e97beee832314b39bca12ad9f04f35a2e52c5c
Author: ysga <ysga168@icloud.com>
Date:   Mon Mar 2 23:01:20 2026 +0800

    init openclaw agent config

commit 317708de4b829466618de4d45715dddd3d8c9dd0
Author: 小千 <agent@local>
Date:   Sun Mar 1 06:50:05 2026 +0000

    auto backup 2026-03-01 06:50:05

commit 0812f25c616a9487f447bc9e8a0a70431a311339
Author: 小千 <agent@local>
Date:   Sun Mar 1 06:49:32 2026 +0000

    auto backup 2026-03-01 06:49:32

commit 390a82e0f2fedfd6611800e548d2cca791a3aab3
Author: 小千 <agent@local>
Date:   Sun Mar 1 06:34:49 2026 +0000

    auto backup 2026-03-01 06:34:49

commit 54cd4fcfc1d075738c4a4c68de4bd9630662f1d6
Author: 小千 <agent@local>
Date:   Sun Mar 1 06:21:20 2026 +0000

    auto backup 2026-03-01 06:21:20

commit 78a59ba6602f844754b310fb4e839acd3758277f
Author: 小千 <agent@local>
Date:   Sun Mar 1 06:20:07 2026 +0000

    auto backup 2026-03-01 06:20:07

commit e7b5306a981b70e8719fb3489ac420ac51e15476
Author: 小千 <agent@local>
Date:   Sun Mar 1 05:55:48 2026 +0000

    backup agent config + skills
    
    - IDENTITY.md: Agent identity (小千)
    - USER.md: User preferences (育董)
    - STATE_PACK.md: Active state and skills
    - MEMORY.md: Long-term memory structure
    - skills/: Adaptive reasoning skill
    - SKILLS_INDEX.md: Skills inventory
    - .gitignore: Exclude logs, memory, secrets
diff --git a/AGENTS.md b/AGENTS.md
index 887a5a8..7ab3196 100644
--- a/AGENTS.md
+++ b/AGENTS.md
@@ -207,6 +207,57 @@ Think of it like a human reviewing their journal and updating their mental model
 
 The goal: Be helpful without being annoying. Check in a few times a day, do useful background work, but respect quiet time.
 
+## Skill Usage Guidelines
+
+### When to Use Which Skill
+
+**For Design & Planning:**
+- `brainstorming` - Before any creative work, feature creation, or system design
+- `adaptive-reasoning` - Automatically adjusts reasoning level based on task complexity
+
+**For Configuration:**
+- `agent-config` - When modifying core context files (AGENTS.md, SOUL.md, etc.)
+- `openclaw-config` - When editing OpenClaw Gateway configuration
+
+**For Context Management:**
+- `context-clean-up` - When context is bloating (audit-only, produces fix plan)
+- `context-hygiene` - Regular context maintenance protocol
+
+**For Browser Automation:**
+- `agent-browser` - For headless browser automation and web scraping
+
+### Skill Priority Order
+1. Use `brainstorming` before implementation
+2. Use `context-clean-up` for periodic audits
+3. Use `agent-config` for behavior tuning
+4. Use `agent-browser` for web automation
+
+### Subagent Delegation Rules
+
+**Spawn a subagent when:**
+- Task requires 3+ tool calls
+- Complex multi-step workflow
+- Heavy exploration/research
+- Isolated testing needed
+- Long-running process (>5 minutes)
+
+**Keep in main session when:**
+- Simple lookups or quick tasks
+- 1-2 tool calls needed
+- User interaction required
+- Context needs to be preserved
+
+**Subagent configuration:**
+```bash
+sessions_spawn(
+    task="Clear task description",
+    label="Descriptive label",
+    runtime="subagent",
+    agentId="main",
+    mode="run"  # or "session" for persistent
+)
+```
+
 ## Make It Yours
 
 This is a starting point. Add your own conventions, style, and rules as you figure out what works.
diff --git a/MEMORY.md b/MEMORY.md
index 29ad8ad..0ae8b17 100644
--- a/MEMORY.md
+++ b/MEMORY.md
@@ -14,6 +14,7 @@
 - 後續規劃：可能使用本地模型批次產出中華民國法條之專有名詞解釋與白話摘要
 - 記憶偏好：希望代理將重點以日期化方式歸檔，便於日後回滾檢索，不必每次重讀全對話
 - 壓縮上下文流程要求：每次完成上下文壓縮後，固定寫入 Obsidian 記憶中樞（至少含日誌+摘要）
+- 記憶中樞固定路徑：`/home/ysga/文件/Obsidian Vault/智研法律AI系統/98_記憶中樞`
 - 接受在 Obsidian 建立專用記憶區，供後續向量化檢索使用
 - 模型策略/流程策略可由代理主動補充到記憶索引（以可執行、可驗證為原則）
 
diff --git a/SKILLS_INDEX.md b/SKILLS_INDEX.md
index 1bec4b2..91efa99 100644
--- a/SKILLS_INDEX.md
+++ b/SKILLS_INDEX.md
@@ -3,4 +3,10 @@
 | Path | Purpose (inferred) | Last Modified |
 |---|---|---|
 | `skills/adaptive-reasoning.md` | name: adaptive-reasoning | 2026-03-05 17:11:55 +0800 |
-| `skills/REGISTRY.md` | Skills Registry | 2026-03-05 17:11:59 +0800 |
+| `skills/brainstorming/SKILL.md` | name: brainstorming | 2026-03-08 16:20:00 +0800 |
+| `skills/agent-config/SKILL.md` | name: agent-config | 2026-03-08 16:26:00 +0800 |
+| `skills/openclaw-config/SKILL.md` | name: openclaw-config | 2026-03-08 16:26:00 +0800 |
+| `skills/context-clean-up/SKILL.md` | name: context-clean-up | 2026-03-08 16:31:00 +0800 |
+| `skills/context-hygiene/SKILL.md` | name: context-hygiene | 2026-03-08 16:31:00 +0800 |
+| `skills/agent-browser/SKILL.md` | name: Agent Browser | 2026-03-08 16:39:00 +0800 |
+| `skills/REGISTRY.md` | Skills Registry | 2026-03-08 16:39:00 +0800 |
diff --git a/TOOLS.md b/TOOLS.md
index 917e2fa..0f4938f 100644
--- a/TOOLS.md
+++ b/TOOLS.md
@@ -29,12 +29,40 @@ Things like:
 
 - Preferred voice: "Nova" (warm, slightly British)
 - Default speaker: Kitchen HomePod
+
+### 記憶中樞 (Memory Hub)
+
+- 記憶中樞路徑: /home/ysga/文件/Obsidian Vault/智研法律AI系統/98_記憶中樞
+- 用途: 集中存放可回滾的會話重點、每日摘要與後續向量化檢索素材
+- 結構: 日誌/、摘要/、索引/
 ```
 
 ## Why Separate?
 
 Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.
 
+### Installed Skills Reference
+
+#### Design & Planning
+- `brainstorming` - Design workflow before implementation
+- `adaptive-reasoning` - Automatic reasoning level adjustment
+
+#### Configuration Management
+- `agent-config` - Core context file modifications
+- `openclaw-config` - Gateway configuration editing
+
+#### Context Management
+- `context-clean-up` - Context bloat audit and fix planning
+- `context-hygiene` - Context maintenance protocol
+
+#### Browser Automation
+- `agent-browser` - Headless browser automation CLI
+
+#### Skill Installation
+- Use `clawhub search <skill-name>` to find skills
+- Use `clawhub install <skill-name>` to install
+- Check `SKILLS_INDEX.md` for installed skills
+
 ---
 
 Add whatever helps you do your job. This is your cheat sheet.
diff --git a/scripts/legal_batch_processor_v4.py b/scripts/legal_batch_processor_v4.py
index 4402349..22c4884 100644
--- a/scripts/legal_batch_processor_v4.py
+++ b/scripts/legal_batch_processor_v4.py
@@ -33,7 +33,9 @@ class ConservativeModelClient:
     
     def __init__(self, base_url: str = "http://127.0.0.1:11434"):
         self.base_url = base_url
-        self.model = "qwen3.5:9b-4k"
+        # 優先使用 deepseek-r1:7b，若不存在則回退到 qwen3.5:9b
+        self.model = "deepseek-r1:7b"
+        self.fallback_model = "qwen3.5:9b"
         self.max_retries = 3
         self.timeout = 180  # 3分鐘
     
@@ -46,9 +48,9 @@ class ConservativeModelClient:
                     "prompt": prompt,
                     "stream": False,
                     "options": {
-                        "temperature": 0.2,  # 更低溫度以提高穩定性
-                        "top_p": 0.8,
-                        "num_predict": 384,  # 較短輸出
+                        "temperature": 0.7,  # 提高溫度以增加多樣性，避免空回應
+                        "top_p": 0.9,
+                        "num_predict": 512,  # 適中輸出長度
                     }
                 }
                 
@@ -92,39 +94,17 @@ class ConservativeModelClient:
     def generate_core_fields(self, law: str, article: str, text: str) -> Optional[Dict[str, str]]:
         """生成核心欄位：白話摘要、規範功能、關鍵字"""
         
-        # 極簡提示，確保模型能處理
-        system_prompt = """你是一個法律條文分析助手。請根據輸入的法條生成以下三個欄位：
-1. 白話摘要：用日常語言解釋條文，禁止複製原文
-2. 規範功能：選擇最合適的分類
-3. 關鍵字：提取3-5個核心術語
-
-請嚴格按照以下格式輸出：
-白話摘要：[解釋]
-規範功能：[分類]
-關鍵字：[詞1 詞2 詞3]"""
-        
-        # 分類說明（在系統提示中）
-        func_categories = [
-            "原則/宣示性規範",
-            "定義條", 
-            "構成要件條",
-            "法律效果條",
-            "程序/救濟條",
-            "組織/權限條",
-            "例外/限制條",
-            "授權/準用條"
-        ]
+        # 簡化提示，避免嚴格格式要求
+        system_prompt = """請用日常語言解釋法律條文，不要複製原文。然後告訴我這條文屬於哪種功能分類，以及列出幾個關鍵詞。"""
         
-        user_prompt = f"""請分析以下法條：
-
-法規：{law}
+        user_prompt = f"""法規：{law}
 條號：{article}
 條文原文：{text}
 
-請生成：
-白話摘要：（用日常語言解釋）
-規範功能：（從上述分類中選擇）
-關鍵字：（3-5個核心術語）"""
+請幫我：
+1. 用白話解釋這條法律在說什麼（不要抄原文）
+2. 告訴我這屬於哪種規範功能
+3. 列出3-5個關鍵詞"""
         
         response = self.generate_with_retry(user_prompt, system_prompt)
         if not response:
@@ -134,13 +114,14 @@ class ConservativeModelClient:
         return self._parse_response(response)
     
     def _parse_response(self, text: str) -> Dict[str, str]:
-        """解析模型回應"""
+        """解析模型回應（支援自由格式）"""
         result = {
             "白話摘要": "",
             "規範功能": "",
             "關鍵字": ""
         }
         
+        # 先嘗試嚴格格式匹配
         lines = text.split('\n')
         
         for line in lines:
@@ -161,6 +142,39 @@ class ConservativeModelClient:
                 sep = ":" if ":" in line else "："
                 result["關鍵字"] = line.split(sep, 1)[1].strip()
         
+        # 如果沒有找到嚴格格式，嘗試自由解析
+        if not result["白話摘要"]:
+            # 尋找可能包含解釋的句子
+            sentences = text.replace('\n', '。').split('。')
+            for sent in sentences:
+                if len(sent) > 10 and ('解釋' in sent or '意思是' in sent or '指' in sent):
+                    result["白話摘要"] = sent.strip()
+                    break
+            if not result["白話摘要"] and len(sentences) > 0:
+                # 使用第一個句子作為白話摘要
+                result["白話摘要"] = sentences[0].strip()
+        
+        if not result["規範功能"]:
+            # 嘗試從文本中識別分類關鍵詞
+            norm_keywords = [
+                "原則/宣示性規範", "定義條", "構成要件條", "法律效果條",
+                "程序/救濟條", "組織/權限條", "例外/限制條", "授權/準用條"
+            ]
+            for kw in norm_keywords:
+                if kw in text:
+                    result["規範功能"] = kw
+                    break
+        
+        if not result["關鍵字"]:
+            # 嘗試提取看起來像關鍵詞的詞語（2-4字）
+            import re
+            words = re.findall(r'[\u4e00-\u9fff]{2,4}', text)
+            # 移除常見虛詞
+            stopwords = ['可以', '應當', '如果', '但是', '以及', '或者', '然後']
+            keywords = [w for w in words if w not in stopwords][:5]
+            if keywords:
+                result["關鍵字"] = ' '.join(keywords)
+        
         return result
 
 class RobustRuleEngine:
diff --git a/skills/REGISTRY.md b/skills/REGISTRY.md
index 1a51c76..9183cb8 100644
--- a/skills/REGISTRY.md
+++ b/skills/REGISTRY.md
@@ -2,3 +2,17 @@
 
 ## Cognitive Preprocessing
 - adaptive-reasoning: skills/adaptive-reasoning.md
+
+## Design & Planning
+- brainstorming: skills/brainstorming/SKILL.md
+
+## Agent Configuration
+- agent-config: skills/agent-config/SKILL.md
+- openclaw-config: skills/openclaw-config/SKILL.md
+
+## Context Management
+- context-clean-up: skills/context-clean-up/SKILL.md
+- context-hygiene: skills/context-hygiene/SKILL.md
+
+## Browser Automation
+- agent-browser: skills/agent-browser/SKILL.md

## 最佳實踐
1. 提交訊息清晰明確
2. 頻繁提交，每次提交一個邏輯單元
3. 使用分支進行功能開發
4. 定期與遠端同步
5. 解決衝突時仔細檢查
