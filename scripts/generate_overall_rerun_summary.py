#!/usr/bin/env python3
"""
生成總體重跑摘要報告
"""

import csv
import sys
import os
import glob
from datetime import datetime
from pathlib import Path
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def generate_summary(rerun_files, summary_dir):
    """生成總體重跑摘要報告"""
    if not rerun_files:
        logger.info("沒有重跑文件需要處理")
        return None
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    summary_path = os.path.join(summary_dir, f"overall_rerun_summary_{timestamp}.txt")
    
    total_rerun = 0
    summary_lines = []
    
    summary_lines.append("=" * 60)
    summary_lines.append(f"總體重跑摘要報告 - {timestamp}")
    summary_lines.append("=" * 60)
    
    for rerun_file in rerun_files:
        if not os.path.exists(rerun_file):
            logger.warning(f"重跑文件不存在: {rerun_file}")
            continue
        
        try:
            with open(rerun_file, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                count = sum(1 for _ in reader)
                total_rerun += count
                
                filename = os.path.basename(rerun_file)
                law_type = filename.split('_')[0] if '_' in filename else filename
                
                summary_lines.append(f"\n{law_type}重跑清單:")
                summary_lines.append(f"  文件: {filename}")
                summary_lines.append(f"  需要重跑條目: {count} 條")
                
                # 重置文件指針重新讀取
                f.seek(0)
                next(reader)  # 跳過標題行
                
                # 顯示前3條
                preview_lines = []
                for i, row in enumerate(reader):
                    if i >= 3:
                        if count > 3:
                            preview_lines.append(f"    還有 {count - 3} 條...")
                        break
                    law = row.get('法規', '')
                    article = row.get('條號', '')
                    issues = row.get('_quality_issues', '無問題')
                    preview_lines.append(f"    {i+1}. {law}{article} - {issues[:50]}...")
                
                if preview_lines:
                    summary_lines.extend(preview_lines)
                    
        except Exception as e:
            logger.error(f"讀取重跑文件失敗 {rerun_file}: {e}")
            summary_lines.append(f"\n{os.path.basename(rerun_file)}: 讀取失敗 - {e}")
    
    summary_lines.append(f"\n{'='*60}")
    summary_lines.append(f"總計需要重跑: {total_rerun} 條")
    
    # 添加建議
    if total_rerun > 0:
        summary_lines.append("\n建議行動:")
        summary_lines.append("1. 檢查模型服務是否正常運行")
        summary_lines.append("2. 確認模型參數設定是否合適")
        summary_lines.append("3. 考慮使用不同模型進行重跑")
        summary_lines.append("4. 檢查條文原文是否有特殊格式")
    
    summary_lines.append("=" * 60)
    
    try:
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(summary_lines))
        
        logger.info(f"總體重跑摘要報告: {summary_path}")
        return summary_path
    except Exception as e:
        logger.error(f"寫入摘要報告失敗: {e}")
        return None

def main():
    """主函數"""
    if len(sys.argv) < 3:
        print("用法: python3 generate_overall_rerun_summary.py <重跑清單文件1> <重跑清單文件2> ... <輸出目錄>")
        print("示例: python3 generate_overall_rerun_summary.py /path/rerun1.csv /path/rerun2.csv /output/dir")
        sys.exit(1)
    
    # 最後一個參數是輸出目錄
    output_dir = sys.argv[-1]
    rerun_files = sys.argv[1:-1]
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    
    result = generate_summary(rerun_files, output_dir)
    if result:
        print(f"✓ 總體重跑摘要已生成: {result}")
    else:
        print("✗ 總體重跑摘要生成失敗")

if __name__ == "__main__":
    main()