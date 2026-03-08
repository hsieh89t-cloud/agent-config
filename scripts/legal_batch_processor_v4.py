#!/usr/bin/env python3
"""
法律條文批次處理器 v3 - 品質與正確性優先
每天凌晨2點執行，專注於穩定批次處理
"""

import csv
import json
import time
import re
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import requests
import logging
import hashlib

# 設定日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/ysga/.openclaw/workspace/logs/legal_processor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ConservativeModelClient:
    """保守型模型客戶端：專注於穩定性和品質"""
    
    def __init__(self, base_url: str = "http://127.0.0.1:11434"):
        self.base_url = base_url
        # 優先使用 deepseek-r1:7b，若不存在則回退到 qwen3.5:9b
        self.model = "deepseek-r1:7b"
        self.fallback_model = "qwen3.5:9b"
        self.max_retries = 3
        self.timeout = 180  # 3分鐘
    
    def generate_with_retry(self, prompt: str, system_prompt: str = None) -> Optional[str]:
        """帶重試的生成"""
        for attempt in range(self.max_retries):
            try:
                payload = {
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,  # 提高溫度以增加多樣性，避免空回應
                        "top_p": 0.9,
                        "num_predict": 512,  # 適中輸出長度
                    }
                }
                
                if system_prompt:
                    payload["system"] = system_prompt
                
                logger.info(f"模型請求 (嘗試 {attempt+1}/{self.max_retries})")
                start_time = time.time()
                
                response = requests.post(
                    f"{self.base_url}/api/generate",
                    json=payload,
                    timeout=self.timeout
                )
                response.raise_for_status()
                result = response.json()
                
                elapsed = time.time() - start_time
                generated_text = result.get("response", "").strip()
                
                logger.info(f"模型回應，耗時: {elapsed:.1f}秒，長度: {len(generated_text)}字元")
                
                if generated_text and len(generated_text) > 10:
                    return generated_text
                else:
                    logger.warning(f"模型返回空或過短回應，等待重試...")
                    time.sleep(2)
                    
            except requests.exceptions.Timeout:
                logger.warning(f"模型請求超時 (嘗試 {attempt+1})")
                if attempt < self.max_retries - 1:
                    time.sleep(5)
            except Exception as e:
                logger.error(f"模型請求錯誤: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(5)
        
        logger.error(f"模型請求失敗，已重試{self.max_retries}次")
        return None
    
    def generate_core_fields(self, law: str, article: str, text: str) -> Optional[Dict[str, str]]:
        """生成核心欄位：白話摘要、規範功能、關鍵字"""
        
        # 簡化提示，避免嚴格格式要求
        system_prompt = """請用日常語言解釋法律條文，不要複製原文。然後告訴我這條文屬於哪種功能分類，以及列出幾個關鍵詞。"""
        
        user_prompt = f"""法規：{law}
條號：{article}
條文原文：{text}

請幫我：
1. 用白話解釋這條法律在說什麼（不要抄原文）
2. 告訴我這屬於哪種規範功能
3. 列出3-5個關鍵詞"""
        
        response = self.generate_with_retry(user_prompt, system_prompt)
        if not response:
            return None
        
        # 解析回應
        return self._parse_response(response)
    
    def _parse_response(self, text: str) -> Dict[str, str]:
        """解析模型回應（支援自由格式）"""
        result = {
            "白話摘要": "",
            "規範功能": "",
            "關鍵字": ""
        }
        
        # 先嘗試嚴格格式匹配
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # 檢查白話摘要
            if line.startswith("白話摘要") and (":" in line or "：" in line):
                sep = ":" if ":" in line else "："
                result["白話摘要"] = line.split(sep, 1)[1].strip()
            
            # 檢查規範功能
            elif line.startswith("規範功能") and (":" in line or "：" in line):
                sep = ":" if ":" in line else "："
                result["規範功能"] = line.split(sep, 1)[1].strip()
            
            # 檢查關鍵字
            elif line.startswith("關鍵字") and (":" in line or "：" in line):
                sep = ":" if ":" in line else "："
                result["關鍵字"] = line.split(sep, 1)[1].strip()
        
        # 如果沒有找到嚴格格式，嘗試自由解析
        if not result["白話摘要"]:
            # 尋找可能包含解釋的句子
            sentences = text.replace('\n', '。').split('。')
            for sent in sentences:
                if len(sent) > 10 and ('解釋' in sent or '意思是' in sent or '指' in sent):
                    result["白話摘要"] = sent.strip()
                    break
            if not result["白話摘要"] and len(sentences) > 0:
                # 使用第一個句子作為白話摘要
                result["白話摘要"] = sentences[0].strip()
        
        if not result["規範功能"]:
            # 嘗試從文本中識別分類關鍵詞
            norm_keywords = [
                "原則/宣示性規範", "定義條", "構成要件條", "法律效果條",
                "程序/救濟條", "組織/權限條", "例外/限制條", "授權/準用條"
            ]
            for kw in norm_keywords:
                if kw in text:
                    result["規範功能"] = kw
                    break
        
        if not result["關鍵字"]:
            # 嘗試提取看起來像關鍵詞的詞語（2-4字）
            import re
            words = re.findall(r'[\u4e00-\u9fff]{2,4}', text)
            # 移除常見虛詞
            stopwords = ['可以', '應當', '如果', '但是', '以及', '或者', '然後']
            keywords = [w for w in words if w not in stopwords][:5]
            if keywords:
                result["關鍵字"] = ' '.join(keywords)
        
        return result

class RobustRuleEngine:
    """穩健規則引擎：基於規則填充其餘欄位"""
    
    @staticmethod
    def classify_norm_function(text: str) -> str:
        """分類規範功能（規則版）"""
        text_clean = text.replace(" ", "").replace("\n", "")
        
        # 關鍵詞匹配
        keyword_mapping = [
            (["稱", "謂", "定義", "指", "係"], "定義條"),
            (["處", "罰", "刑", "拘役", "有期徒刑"], "法律效果條"),
            (["但", "不在此限", "除外", "過當"], "例外/限制條"),
            (["以", "意圖", "著手", "實施", "違反", "未經"], "構成要件條"),
            (["得提起", "應通知", "期限", "程序", "救濟"], "程序/救濟條"),
            (["機關", "權限", "職權", "組成", "任期"], "組織/權限條"),
            (["由", "授權", "準用", "依", "參照"], "授權/準用條"),
            (["為", "基於", "屬於", "原則", "共和國"], "原則/宣示性規範"),
        ]
        
        for keywords, category in keyword_mapping:
            if any(kw in text_clean for kw in keywords):
                return category
        
        return "原則/宣示性規範"
    
    @staticmethod
    def should_use_v2_format(norm_func: str, text: str) -> bool:
        """判斷是否使用 v2 高價值版格式"""
        # 根據 v2.1 規範的分流規則：
        # v2 高價值版：民法責任條、刑法構成要件條、行政程序效果條、核心救濟條
        # 對應的規範功能分類：
        # - 構成要件條：刑法構成要件條
        # - 法律效果條：行政程序效果條、核心救濟條
        # - 例外/限制條：部分核心責任條
        # - 程序/救濟條：救濟程序相關
        
        v2_functions = [
            "構成要件條",     # 刑法構成要件條
            "法律效果條",     # 行政程序效果條、核心救濟條
            "例外/限制條",    # 部分核心責任條
            "程序/救濟條"     # 救濟程序相關
        ]
        
        # 如果是這些分類，使用 v2 格式
        if norm_func in v2_functions:
            return True
        
        # 額外檢查：條文包含特定關鍵詞
        v2_keywords = [
            "責任", "處罰", "刑", "賠償", "損害", "侵權", 
            "違約", "犯罪", "構成", "要件", "效果", "救濟"
        ]
        
        # 如果條文包含高價值關鍵詞，也使用 v2 格式
        text_clean = text.replace(" ", "").replace("\n", "")
        for keyword in v2_keywords:
            if keyword in text_clean:
                return True
        
        return False
    
    @staticmethod
    def extract_keywords(text: str) -> str:
        """提取關鍵字（規則版）"""
        # 法律常見關鍵詞
        legal_keywords = [
            "防衛", "避難", "未遂", "中止", "共犯", "教唆", "幫助",
            "不罰", "減輕", "免除", "犯罪", "行為", "結果", "危險",
            "侵害", "權利", "義務", "責任", "處罰", "刑罰", "法律",
            "條文", "規定", "適用", "解釋", "爭議", "正當", "緊急",
            "過當", "合法", "違法", "構成", "要件", "效果", "制裁"
        ]
        
        found = []
        for kw in legal_keywords:
            if kw in text and kw not in found:
                found.append(kw)
                if len(found) >= 5:
                    break
        
        return " ".join(found) if found else "法律規範"
    
    @staticmethod
    def generate_core_requirements(text: str, norm_func: str) -> str:
        """生成核心要件"""
        if "防衛" in text:
            return "1. 存在現在不法之侵害\n2. 出於防衛意思\n3. 實施防衛行為"
        elif "避難" in text:
            return "1. 面臨緊急危難\n2. 出於不得已\n3. 為避免自己或他人生命身體自由財產之危險"
        elif "未遂" in text:
            return "1. 已著手於犯罪行為之實行\n2. 行為不遂"
        elif "中止" in text:
            return "1. 已著手於犯罪行為\n2. 因己意中止\n3. 防止結果發生"
        elif norm_func == "構成要件條":
            return "1. 具備主觀要素\n2. 符合客觀要件\n3. 無阻卻違法事由"
        else:
            return ""  # 無具體要件時留空
    
    @staticmethod
    def generate_legal_effects(text: str, norm_func: str) -> str:
        """生成法律效果"""
        effects = []
        
        if "不罰" in text:
            effects.append("不處罰")
        if "減輕" in text:
            effects.append("得減輕刑罰")
        if "免除" in text:
            effects.append("得免除刑罰")
        if "處" in text and "刑" in text:
            # 嘗試提取刑度
            match = re.search(r"處(.{1,10}?刑)", text)
            if match:
                effects.append(f"處{match.group(1)}刑")
            else:
                effects.append("處以刑罰")
        
        if effects:
            return "\n".join(f"{i+1}. {effect}" for i, effect in enumerate(effects))
        
        if norm_func == "法律效果條":
            return "1. 產生法律制裁效果\n2. 影響當事人權利義務"
        else:
            return ""
    
    @staticmethod
    def generate_application_scenario(law: str, article: str, text: str) -> str:
        """生成適用情境"""
        # 刑法特定條文
        scenarios = {
            "第23條": "被攻擊時反擊是否合法；防衛行為是否過當；自衛造成傷害的責任認定。",
            "第24條": "緊急情況下損害他人財產是否免責；避難行為的合理限度；危難救助的法律邊界。",
            "第25條": "犯罪未完成的處罰；未遂與既遂的區別；未遂犯的刑度計算。",
            "第26條": "行為不可能成功是否構成犯罪；不能犯的處理；迷信犯的法律評價。",
            "第27條": "犯罪中途停止的後果；中止犯的減刑條件；主動防止結果發生的認定。",
            "第28條": "共同犯罪的責任分擔；正犯與共犯的區別；犯罪團體中的個人責任。",
            "第29條": "教唆他人犯罪的責任；教唆犯的構成要件；教唆未遂的處理。",
            "第30條": "幫助犯罪的責任；幫助犯的認定標準；間接幫助的法律效果。",
        }
        
        if article in scenarios:
            return scenarios[article]
        
        # 通用場景
        if "防衛" in text:
            return "自衛情況下的法律責任；防衛限度的判斷；緊急狀況下的行為合法性。"
        elif "避難" in text:
            return "緊急危難下的行為選擇；避難造成的損害賠償；危急情況的法律例外。"
        elif law == "中華民國憲法":
            return "憲法原則的適用；基本權利的保障；國家組織的權限劃分。"
        elif law == "民法":
            return "民事法律關係的建立與變更；權利義務的界定；損害賠償的計算。"
        elif law == "刑法":
            return "犯罪構成要件的判斷；刑罰的適用與裁量；刑事責任的認定。"
        else:
            return "法律條文的解釋與適用；相關案件的法律分析；權利義務的具體化。"
    
    @staticmethod
    def generate_rag_queries(law: str, article: str, plain_summary: str) -> str:
        """生成RAG檢索句"""
        queries = []
        
        # 基本查詢
        queries.append(f"{law}{article}在說什麼？")
        queries.append(f"違反{law}{article}會怎樣？")
        
        # 情境查詢
        if "防衛" in plain_summary:
            queries.append("被打還手算正當防衛嗎？")
        elif "避難" in plain_summary:
            queries.append("緊急情況下可以破壞別人東西嗎？")
        elif "未遂" in plain_summary:
            queries.append("犯罪沒成功會處罰嗎？")
        elif "中止" in plain_summary:
            queries.append("犯罪到一半停止會怎樣？")
        
        # 確保有3個查詢
        while len(queries) < 3:
            queries.append(f"{law}{article}的實際案例有哪些？")
        
        return "\n".join(f"{i+1}. {q}" for i, q in enumerate(queries[:3]))
    
    @staticmethod
    def generate_legal_purpose(norm_func: str) -> str:
        """生成法理與制度目的"""
        purposes = {
            "原則/宣示性規範": "確立法律基本原則與價值取向，指引法律適用方向。",
            "定義條": "明確法律用語內涵，統一解釋標準，避免適用歧異。",
            "構成要件條": "界定行為模式與法律要件，提供明確的判斷基準。",
            "法律效果條": "規定違反法律之效果，確保法律之實效性與威懾力。",
            "程序/救濟條": "規範權利實現程序，保障程序正義與權利救濟。",
            "組織/權限條": "劃分機關職權，確保權力分立與制衡機制。",
            "例外/限制條": "平衡不同法益，設定原則之例外或合理限制。",
            "授權/準用條": "保持法律彈性，授權細化規範或準用既有規定。"
        }
        
        return purposes.get(norm_func, "實現法律規範目的，保障權利義務關係。")
    
    @staticmethod
    def generate_practice_issues(text: str) -> str:
        """生成實務爭點"""
        if "防衛" in text and "過當" in text:
            return "防衛是否『現在』的判斷；防衛行為是否『過當』的標準；防衛意思的證明。"
        elif "避難" in text:
            return "危難是否『緊急』的認定；避難行為是否『不得已』的判斷；避難過當的標準。"
        elif "未遂" in text:
            return "『著手』的認定標準；未遂犯的處罰範圍；不能犯的處理方式。"
        elif "中止" in text:
            return "『己意』中止的認定；防止結果發生的有效性；中止犯的減免標準。"
        else:
            return "條文解釋與適用範圍；與相關條文的關係；具體案例中的判斷標準。"
    
    @staticmethod
    def generate_legal_structure(text: str, norm_func: str) -> str:
        """生成法律結構圖（v2 高價值版專用）"""
        if norm_func not in ["構成要件條", "法律效果條", "例外/限制條", "程序/救濟條"]:
            return ""
        
        structure_parts = []
        
        # 規範前提
        if "防衛" in text:
            structure_parts.append("規範前提：存在現在不法之侵害")
        elif "避難" in text:
            structure_parts.append("規範前提：面臨緊急危難")
        elif "未遂" in text:
            structure_parts.append("規範前提：已著手於犯罪行為之實行")
        elif "中止" in text:
            structure_parts.append("規範前提：已著手於犯罪行為")
        
        # 核心要件
        requirements = RobustRuleEngine.generate_core_requirements(text, norm_func)
        if requirements:
            structure_parts.append("核心要件：")
            structure_parts.append(requirements)
        
        # 法律效果
        effects = RobustRuleEngine.generate_legal_effects(text, norm_func)
        if effects:
            structure_parts.append("法律效果：")
            structure_parts.append(effects)
        
        # 例外限制
        if "但" in text or "不在此限" in text or "除外" in text:
            structure_parts.append("例外限制：但書條款限制適用範圍")
        
        if structure_parts:
            return "\n".join(structure_parts)
        return ""
    
    @staticmethod
    def generate_reasoning_chain(text: str, norm_func: str) -> str:
        """生成條文推理鏈（v2 高價值版專用）"""
        if norm_func not in ["構成要件條", "法律效果條", "例外/限制條", "程序/救濟條"]:
            return ""
        
        # 簡單推理鏈生成
        if "防衛" in text and "過當" in text:
            return "若存在現在不法之侵害 → 可實施防衛行為 → 但防衛過當時 → 得減輕或免除其刑"
        elif "避難" in text:
            return "若面臨緊急危難 → 出於不得已實施避難行為 → 避難過當時 → 得減輕或免除其刑"
        elif "未遂" in text:
            return "若已著手於犯罪行為 → 但行為不遂 → 仍構成未遂犯 → 得按既遂犯之刑減輕"
        elif "中止" in text:
            return "若已著手於犯罪行為 → 因己意中止 → 且防止結果發生 → 得減輕或免除其刑"
        elif norm_func == "構成要件條":
            return "若符合構成要件 → 且無阻卻違法事由 → 則行為具有違法性"
        elif norm_func == "法律效果條":
            return "若行為違法 → 則產生相應法律效果 → 影響當事人權利義務"
        else:
            return ""

class QualityController:
    """品質控制器"""
    
    @staticmethod
    def validate_plain_summary(plain: str, original: str) -> Tuple[bool, str]:
        """驗證白話摘要"""
        if not plain or len(plain.strip()) < 10:
            return False, "白話摘要過短或為空"
        
        if plain == original or plain in original:
            return False, "白話摘要複製原文"
        
        # 檢查是否包含足夠的解釋性詞語
        explanatory_words = ["意思", "是指", "代表", "可以", "應該", "必須", "不會", "可以", "得"]
        if not any(word in plain for word in explanatory_words):
            return False, "白話摘要缺乏解釋性內容"
        
        return True, "OK"
    
    @staticmethod
    def validate_norm_function(func: str) -> Tuple[bool, str]:
        """驗證規範功能"""
        valid_funcs = [
            "原則/宣示性規範", "定義條", "構成要件條", "法律效果條",
            "程序/救濟條", "組織/權限條", "例外/限制條", "授權/準用條"
        ]
        
        if not func:
            return False, "規範功能為空"
        
        if func not in valid_funcs:
            return False, f"規範功能'{func}'不在有效分類中"
        
        return True, "OK"
    
    @staticmethod
    def validate_keywords(keywords: str) -> Tuple[bool, str]:
        """驗證關鍵字"""
        if not keywords or len(keywords.strip()) < 2:
            return False, "關鍵字為空或過短"
        
        if keywords == "法律規範" or keywords == "法律條文":
            return False, "關鍵字為默認值"
        
        # 至少應有2個關鍵字
        kw_list = keywords.split()
        if len(kw_list) < 2:
            return False, "關鍵字數量不足"
        
        return True, "OK"

class BatchProcessor:
    """批次處理器"""
    
    def __init__(self, input_csv: str, output_dir: str):
        self.input_csv = input_csv
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.model_client = ConservativeModelClient()
        self.rule_engine = RobustRuleEngine()
        self.quality_controller = QualityController()
        
        # 統計
        self.stats = {
            "total": 0,
            "success": 0,
            "failed": 0,
            "model_failures": 0,
            "quality_issues": 0
        }
    
    def load_articles(self, limit: int = None) -> List[Dict]:
        """載入條文"""
        articles = []
        
        try:
            with open(self.input_csv, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                
                for i, row in enumerate(reader):
                    if limit and i >= limit:
                        break
                    
                    # 提取必要欄位
                    unique_id = row.get('Unique_ID', f'ROW_{i+1}')
                    law_name = row.get('法規名稱', '').strip()
                    article_no = row.get('條號', '').strip()
                    # 條文原文不可改寫：保留原始文本（僅移除末端換行）
                    article_text = (row.get('條文內容', '') or '').rstrip('\r\n')
                    
                    # 基本驗證
                    if not law_name or not article_no or not article_text:
                        logger.warning(f"跳過無效行 {i+1}: 缺少必要欄位")
                        continue
                    
                    text_hash = hashlib.sha256(article_text.encode('utf-8')).hexdigest()
                    articles.append({
                        "unique_id": unique_id,
                        "law_name": law_name,
                        "article_no": article_no,
                        "article_text": article_text,
                        "source_text_hash": text_hash,
                        "row_index": i
                    })
            
            logger.info(f"從 {self.input_csv} 載入 {len(articles)} 條有效條文")
            return articles
            
        except Exception as e:
            logger.error(f"載入CSV失敗: {e}")
            return []
    
    def process_article(self, article: Dict) -> Optional[Dict]:
        """處理單一條文"""
        law = article["law_name"]
        article_no = article["article_no"]
        text = article["article_text"]
        
        logger.info(f"處理: {law}{article_no} (ID: {article['unique_id']})")
        
        # 步驟1: 模型生成核心欄位
        logger.info("  步驟1: 模型生成核心欄位...")
        core_fields = self.model_client.generate_core_fields(law, article_no, text)
        
        model_failed = False

        # 如果模型失敗，使用規則引擎（但不再複製條文原文）
        if not core_fields:
            logger.warning("  模型生成失敗，使用規則引擎回退（白話摘要留空待重跑）")
            self.stats["model_failures"] += 1
            model_failed = True
            core_fields = {
                "白話摘要": "",
                "規範功能": self.rule_engine.classify_norm_function(text),
                "關鍵字": self.rule_engine.extract_keywords(text)
            }
        
        # 品質驗證
        quality_ok = True
        quality_issues = []
        
        # 驗證白話摘要
        plain_ok, plain_msg = self.quality_controller.validate_plain_summary(
            core_fields.get("白話摘要", ""), text
        )
        if not plain_ok:
            quality_ok = False
            quality_issues.append(f"白話摘要: {plain_msg}")
        
        # 驗證規範功能
        func_ok, func_msg = self.quality_controller.validate_norm_function(
            core_fields.get("規範功能", "")
        )
        if not func_ok:
            quality_ok = False
            quality_issues.append(f"規範功能: {func_msg}")
        
        # 驗證關鍵字
        kw_ok, kw_msg = self.quality_controller.validate_keywords(
            core_fields.get("關鍵字", "")
        )
        if not kw_ok:
            quality_issues.append(f"關鍵字: {kw_msg}")  # 只警告，不失敗
        
        if quality_issues:
            self.stats["quality_issues"] += 1
            logger.warning(f"  品質問題: {quality_issues}")
        
        # 步驟2: 規則引擎填充其餘欄位
        logger.info("  步驟2: 規則引擎填充其餘欄位...")
        full_output = self._generate_full_output(article, core_fields)

        # 條文不可改寫哨兵：輸出前比對原文雜湊
        if full_output:
            out_hash = hashlib.sha256((full_output.get("條文原文", "") or "").encode("utf-8")).hexdigest()
            if out_hash != article.get("source_text_hash"):
                logger.error(f"  條文原文異動偵測: {law}{article_no}，已阻擋寫出")
                self.stats["failed"] += 1
                return None
        
        # 記錄處理結果
        if full_output:
            # 需重跑旗標：模型失敗或摘要品質未過
            needs_regen = model_failed or (not plain_ok)
            full_output["needs_regen"] = "1" if needs_regen else "0"
            full_output["_quality_issues"] = "; ".join(quality_issues) if quality_issues else ""
            full_output["_processed_at"] = datetime.now().isoformat()
            self.stats["success"] += 1
            return full_output
        else:
            self.stats["failed"] += 1
            return None
    
    def _generate_full_output(self, article: Dict, core_fields: Dict) -> Dict:
        """生成完整輸出（支援 v1/v2 分流）"""
        law = article["law_name"]
        article_no = article["article_no"]
        text = article["article_text"]
        
        plain = core_fields.get("白話摘要", "")
        norm_func = core_fields.get("規範功能", "")
        keywords = core_fields.get("關鍵字", "")
        
        # 確保規範功能有效
        if not norm_func or norm_func not in [
            "原則/宣示性規範", "定義條", "構成要件條", "法律效果條",
            "程序/救濟條", "組織/權限條", "例外/限制條", "授權/準用條"
        ]:
            norm_func = self.rule_engine.classify_norm_function(text)
        
        # 確保關鍵字有效
        if not keywords or keywords == "法律規範":
            keywords = self.rule_engine.extract_keywords(text)
        
        # 判斷是否使用 v2 高價值版格式
        use_v2 = self.rule_engine.should_use_v2_format(norm_func, text)
        
        # 生成通用欄位
        base_fields = {
            "Unique_ID": article["unique_id"],
            "法規": law,
            "條號": article_no,
            "條文原文": text,
            "條文原文SHA256": article.get("source_text_hash", ""),
            "白話摘要": plain,
            "規範功能": norm_func,
            "法理與制度目的": self.rule_engine.generate_legal_purpose(norm_func),
            "核心要件": self.rule_engine.generate_core_requirements(text, norm_func),
            "法律效果": self.rule_engine.generate_legal_effects(text, norm_func),
            "適用情境": self.rule_engine.generate_application_scenario(law, article_no, text),
            "實務爭點": self.rule_engine.generate_practice_issues(text),
            "關鍵字": keywords,
            "法律主題": law.replace("中華民國", "").replace("法", "").strip() or "法律",
            "RAG檢索句": self.rule_engine.generate_rag_queries(law, article_no, plain)
        }
        
        # v1/v2 分流處理
        if use_v2:
            # v2 高價值版：添加額外欄位
            base_fields["格式版本"] = "v2"
            base_fields["法律結構圖"] = self.rule_engine.generate_legal_structure(text, norm_func)
            base_fields["條文推理鏈"] = self.rule_engine.generate_reasoning_chain(text, norm_func)
            # 使用詳細關聯條文（暫時使用基本關聯）
            base_fields["關聯條文"] = self._generate_related_articles(law, article_no, text)
            # 法條定位（簡單實現）
            if law == "中華民國刑法" and "第" in article_no:
                base_fields["法條定位"] = f"刑法總則第{article_no[1:-1]}條"
            elif law == "中華民國民法" and "第" in article_no:
                base_fields["法條定位"] = f"民法第{article_no[1:-1]}條"
            else:
                base_fields["法條定位"] = f"{law}{article_no}"
        else:
            # v1 精簡版
            base_fields["格式版本"] = "v1"
            base_fields["關聯條文"] = self._generate_related_articles(law, article_no, text)
        
        return base_fields
    
    def _compress_and_store_context(self, batch_name: str, results: List[Dict], output_file: Optional[str], elapsed_time: float) -> str:
        """壓縮上下文摘要並存放"""
        try:
            # 統計 v1/v2 分布
            v1_count = 0
            v2_count = 0
            for result in results:
                if result.get("格式版本") == "v2":
                    v2_count += 1
                else:
                    v1_count += 1
            
            # 收集品質問題
            quality_issues = []
            for result in results:
                issues = result.get("_quality_issues", "")
                if issues:
                    quality_issues.append({
                        "unique_id": result.get("Unique_ID", ""),
                        "issues": issues
                    })
            
            # 建構摘要
            summary = {
                "batch_name": batch_name,
                "timestamp": datetime.now().isoformat(),
                "processing_time_seconds": round(elapsed_time, 2),
                "stats": self.stats.copy(),
                "format_distribution": {
                    "v1": v1_count,
                    "v2": v2_count,
                    "v2_percentage": round(v2_count / max(len(results), 1) * 100, 1) if results else 0
                },
                "quality_issues_summary": {
                    "total_articles_with_issues": len(quality_issues),
                    "issues": quality_issues[:10]  # 最多10條
                },
                "output_files": {
                    "csv": output_file,
                    "stats": str(self.output_dir / f"{batch_name}_stats.json")
                },
                "context_compressed": True
            }
            
            # 保存摘要文件
            summary_dir = Path("/home/ysga/.openclaw/workspace/logs/summaries")
            summary_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            summary_file = summary_dir / f"{batch_name}_summary_{timestamp}.json"
            
            with open(summary_file, 'w', encoding='utf-8') as f:
                json.dump(summary, f, ensure_ascii=False, indent=2)
            
            logger.info(f"上下文摘要已壓縮並存放至: {summary_file}")
            
            # 同時生成簡明文字摘要
            text_summary = f"""# 批次處理上下文摘要
批次名稱: {batch_name}
處理時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
總耗時: {elapsed_time:.1f}秒
處理條數: {self.stats['success']}/{self.stats['total']} (成功率: {self.stats['success']/max(self.stats['total'],1)*100:.1f}%)
格式分布: v1={v1_count}, v2={v2_count} (v2佔比: {round(v2_count / max(len(results), 1) * 100, 1)}%)
模型失敗: {self.stats['model_failures']}
品質問題: {self.stats['quality_issues']}
輸出文件: {output_file}
"""
            text_summary_file = summary_dir / f"{batch_name}_summary_{timestamp}.txt"
            with open(text_summary_file, 'w', encoding='utf-8') as f:
                f.write(text_summary)
            
            logger.info(f"文字摘要已保存: {text_summary_file}")
            
            # 同時存放到記憶中樞
            memory_hub_path = self._store_to_memory_hub(batch_name, summary, text_summary, results)
            if memory_hub_path:
                logger.info(f"摘要已同步至記憶中樞: {memory_hub_path}")
            
            return str(summary_file)
            
        except Exception as e:
            logger.error(f"壓縮上下文摘要失敗: {e}")
            return ""
    
    def _store_to_memory_hub(self, batch_name: str, summary: Dict, text_summary: str, results: List[Dict]) -> str:
        """將摘要存放到記憶中樞"""
        try:
            # 記憶中樞路徑
            memory_hub_dir = Path("/home/ysga/文件/Obsidian Vault/智研法律AI系統/98_記憶中樞")
            
            # 1. 創建批次執行日誌（在「日誌」目錄中）
            today = datetime.now().strftime("%Y-%m-%d")
            batch_log_dir = memory_hub_dir / "日誌" / "批次執行"
            batch_log_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            batch_log_file = batch_log_dir / f"{batch_name}_{timestamp}.md"
            
            # 批次執行日誌內容
            batch_log_content = f"""# {batch_name} 批次執行摘要
執行時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
批次名稱: {batch_name}

## 執行統計
- 總條數: {self.stats['total']}
- 成功條數: {self.stats['success']}
- 成功率: {self.stats['success']/max(self.stats['total'],1)*100:.1f}%
- 模型失敗: {self.stats['model_failures']}
- 品質問題: {self.stats['quality_issues']}
- 處理耗時: {summary.get('processing_time_seconds', 0):.1f}秒

## 格式分布
- v1 精簡版: {summary.get('format_distribution', {}).get('v1', 0)} 條
- v2 高價值版: {summary.get('format_distribution', {}).get('v2', 0)} 條
- v2 佔比: {summary.get('format_distribution', {}).get('v2_percentage', 0):.1f}%

## 輸出文件
- CSV 輸出: {summary.get('output_files', {}).get('csv', '')}
- 統計文件: {summary.get('output_files', {}).get('stats', '')}

## 品質問題摘要
"""
            
            # 添加品質問題
            quality_issues = summary.get('quality_issues_summary', {}).get('issues', [])
            if quality_issues:
                for issue in quality_issues[:5]:  # 最多5條
                    batch_log_content += f"- {issue.get('unique_id', '')}: {issue.get('issues', '')}\n"
            else:
                batch_log_content += "- 無品質問題\n"
            
            # 添加處理條文清單（前5條）
            batch_log_content += f"\n## 處理條文清單（共 {len(results)} 條）\n"
            for i, result in enumerate(results[:5]):
                batch_log_content += f"{i+1}. {result.get('法規', '')}{result.get('條號', '')} - {result.get('規範功能', '')}\n"
            if len(results) > 5:
                batch_log_content += f"... 等 {len(results)} 條\n"
            
            # 保存批次執行日誌
            with open(batch_log_file, 'w', encoding='utf-8') as f:
                f.write(batch_log_content)
            
            # 2. 將文字摘要添加到「摘要」目錄
            summary_dir = memory_hub_dir / "摘要" / "批次處理"
            summary_dir.mkdir(parents=True, exist_ok=True)
            
            summary_file = summary_dir / f"{batch_name}_{timestamp}.md"
            with open(summary_file, 'w', encoding='utf-8') as f:
                f.write(text_summary)
            
            # 3. 更新索引文件（如果不存在則創建）
            index_file = memory_hub_dir / "索引" / "批次處理索引.md"
            if not index_file.exists():
                index_content = """# 批次處理索引

## 批次處理系統概述
- 系統版本: v4 (2026-03-07)
- 核心功能: 法律條文自動化結構化處理
- 執行頻率: 每日 02:00 AM
- 處理量: 每法域 20條/天，總計 60條/天
- 格式支援: v1 精簡版 / v2 高價值版 智能分流

## 批次執行記錄
"""
            else:
                with open(index_file, 'r', encoding='utf-8') as f:
                    index_content = f.read()
            
            # 添加本次執行記錄
            index_entry = f"""
### {batch_name} ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
- 條數: {self.stats['success']}/{self.stats['total']} (成功率: {self.stats['success']/max(self.stats['total'],1)*100:.1f}%)
- 格式分布: v1={summary.get('format_distribution', {}).get('v1', 0)}, v2={summary.get('format_distribution', {}).get('v2', 0)}
- 耗時: {summary.get('processing_time_seconds', 0):.1f}秒
- 日誌文件: `日誌/批次執行/{batch_name}_{timestamp}.md`
- 摘要文件: `摘要/批次處理/{batch_name}_{timestamp}.md`
"""
            
            # 確保有「批次執行記錄」章節
            if "## 批次執行記錄" not in index_content:
                index_content += "\n## 批次執行記錄\n"
            
            # 在「批次執行記錄」章節後添加新記錄
            lines = index_content.split('\n')
            new_lines = []
            for line in lines:
                new_lines.append(line)
                if line.strip() == "## 批次執行記錄":
                    new_lines.append(index_entry)
            
            index_content = '\n'.join(new_lines)
            
            with open(index_file, 'w', encoding='utf-8') as f:
                f.write(index_content)
            
            return str(batch_log_file)
            
        except Exception as e:
            logger.error(f"存放到記憶中樞失敗: {e}")
            return ""
    
    def _generate_related_articles(self, law: str, article: str, text: str) -> str:
        """生成關聯條文"""
        if law == "中華民國刑法":
            if "第23條" in article or "防衛" in text:
                return "刑法第24條（緊急避難）"
            elif "第24條" in article or "避難" in text:
                return "刑法第23條（正當防衛）"
            elif "第25條" in article or "未遂" in text:
                return "刑法第26條（不能犯）、第27條（中止犯）"
            elif "第26條" in article or "不能" in text:
                return "刑法第25條（未遂犯）"
            elif "第27條" in article or "中止" in text:
                return "刑法第25條（未遂犯）"
        
        return "與本法相關條文及體系性規範"
    
    def save_results(self, results: List[Dict], batch_name: str):
        """保存結果"""
        if not results:
            logger.warning("無結果可保存")
            return None
        
        # 生成輸出文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = self.output_dir / f"{batch_name}_{timestamp}.csv"
        
        # 確定所有欄位
        all_fields = set()
        for result in results:
            all_fields.update(result.keys())
        
        # 標準化欄位順序
        field_order = [
            'Unique_ID', '法規', '條號', '條文原文', '條文原文SHA256', '白話摘要',
            '規範功能', '法理與制度目的', '核心要件', '法律效果',
            '適用情境', '實務爭點', '關鍵字', '法律主題',
            '關聯條文', 'RAG檢索句', 'needs_regen', '_quality_issues', '_processed_at'
        ]
        
        # 添加其他欄位
        for field in all_fields:
            if field not in field_order:
                field_order.append(field)
        
        try:
            with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=field_order)
                writer.writeheader()
                
                for result in results:
                    writer.writerow(result)
            
            logger.info(f"結果已保存至: {output_file}")
            return str(output_file)
            
        except Exception as e:
            logger.error(f"保存結果失敗: {e}")
            return None
    
    def save_stats(self, batch_name: str):
        """保存統計信息"""
        stats_file = self.output_dir / f"{batch_name}_stats.json"
        
        stats_data = {
            "batch_name": batch_name,
            "timestamp": datetime.now().isoformat(),
            "stats": self.stats,
            "success_rate": self.stats["success"] / max(self.stats["total"], 1) * 100
        }
        
        try:
            with open(stats_file, 'w', encoding='utf-8') as f:
                json.dump(stats_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"統計信息已保存至: {stats_file}")
            return str(stats_file)
            
        except Exception as e:
            logger.error(f"保存統計信息失敗: {e}")
            return None
    
    def run(self, limit: int = 10, batch_name: str = "batch"):
        """執行批次處理"""
        logger.info(f"開始批次處理: {batch_name}")
        logger.info(f"輸入文件: {self.input_csv}")
        logger.info(f"限制條數: {limit}")
        
        # 載入條文
        articles = self.load_articles(limit)
        self.stats["total"] = len(articles)
        
        if not articles:
            logger.error("無有效條文可處理")
            return False
        
        # 處理每條
        results = []
        start_time = time.time()
        
        for i, article in enumerate(articles, 1):
            logger.info(f"處理進度: {i}/{len(articles)}")
            
            result = self.process_article(article)
            if result:
                results.append(result)
            
            # 進度間隔
            if i < len(articles):
                time.sleep(1)  # 避免過載
        
        elapsed = time.time() - start_time
        
        # 保存結果
        output_file = self.save_results(results, batch_name)
        stats_file = self.save_stats(batch_name)
        
        # 輸出總結
        logger.info(f"批次處理完成!")
        logger.info(f"總耗時: {elapsed:.1f}秒")
        logger.info(f"處理速度: {elapsed/max(len(articles),1):.1f}秒/條")
        logger.info(f"統計: {self.stats['success']}/{self.stats['total']} 成功")
        logger.info(f"成功率: {self.stats['success']/max(self.stats['total'],1)*100:.1f}%")
        logger.info(f"模型失敗: {self.stats['model_failures']}")
        logger.info(f"品質問題: {self.stats['quality_issues']}")
        
        if output_file:
            logger.info(f"輸出文件: {output_file}")
        
        # 壓縮上下文摘要並存放
        self._compress_and_store_context(batch_name, results, output_file, elapsed)
        
        return self.stats["success"] > 0

def main():
    """主函數：用於命令行執行"""
    import argparse
    
    parser = argparse.ArgumentParser(description='法律條文批次處理器 v3')
    parser.add_argument('--input', '-i', required=True, help='輸入CSV路徑')
    parser.add_argument('--output-dir', '-o', required=True, help='輸出目錄')
    parser.add_argument('--limit', '-l', type=int, default=10, help='處理條數限制')
    parser.add_argument('--batch-name', '-n', default='legal_batch', help='批次名稱')
    
    args = parser.parse_args()
    
    # 確保輸出目錄存在
    os.makedirs(args.output_dir, exist_ok=True)
    
    # 創建處理器並執行
    processor = BatchProcessor(args.input, args.output_dir)
    success = processor.run(args.limit, args.batch_name)
    
    if success:
        print(f"✓ 批次處理成功完成")
        sys.exit(0)
    else:
        print(f"✗ 批次處理失敗或無結果")
        sys.exit(1)

if __name__ == "__main__":
    main()