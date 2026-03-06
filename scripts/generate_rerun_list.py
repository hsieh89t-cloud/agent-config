#!/usr/bin/env python3
"""
生成重跑清單工具
從批次處理輸出CSV中提取 needs_regen=1 的條目，生成可重跑的清單
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

def find_latest_csv(directory: str) -> str:
    """找到目錄中最新的CSV文件"""
    csv_files = glob.glob(os.path.join(directory, "*.csv"))
    if not csv_files:
        return None
    
    # 按修改時間排序
    csv_files.sort(key=os.path.getmtime, reverse=True)
    return csv_files[0]

def generate_rerun_list(output_csv: str, output_dir: str, batch_name: str) -> str:
    """生成重跑清單"""
    if not output_csv or not os.path.exists(output_csv):
        logger.warning(f"輸出CSV文件不存在: {output_csv}")
        return None
    
    rerun_entries = []
    
    try:
        with open(output_csv, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                # 檢查是否需要重跑
                if row.get('needs_regen') == '1':
                    # 提取必要欄位
                    rerun_entry = {
                        'Unique_ID': row.get('Unique_ID', ''),
                        '法規': row.get('法規', ''),
                        '條號': row.get('條號', ''),
                        '條文原文': row.get('條文原文', ''),
                        '條文原文SHA256': row.get('條文原文SHA256', ''),
                        '白話摘要': row.get('白話摘要', ''),
                        '規範功能': row.get('規範功能', ''),
                        '_quality_issues': row.get('_quality_issues', ''),
                        '_processed_at': row.get('_processed_at', ''),
                        'needs_regen': row.get('needs_regen', ''),
                        '來源輸出文件': os.path.basename(output_csv)
                    }
                    rerun_entries.append(rerun_entry)
        
        if not rerun_entries:
            logger.info("沒有需要重跑的條目")
            return None
        
        # 生成重跑清單文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        rerun_filename = f"{batch_name}_rerun_{timestamp}.csv"
        rerun_path = os.path.join(output_dir, rerun_filename)
        
        # 定義欄位順序
        fieldnames = [
            'Unique_ID', '法規', '條號', '條文原文', '條文原文SHA256',
            '白話摘要', '規範功能', '_quality_issues', '_processed_at',
            'needs_regen', '來源輸出文件'
        ]
        
        with open(rerun_path, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rerun_entries)
        
        logger.info(f"生成重跑清單: {rerun_path} (共 {len(rerun_entries)} 條)")
        return rerun_path
        
    except Exception as e:
        logger.error(f"生成重跑清單失敗: {e}")
        return None

def generate_rerun_summary(rerun_lists: list, summary_dir: str) -> str:
    """生成重跑摘要報告"""
    if not rerun_lists:
        return None
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    summary_path = os.path.join(summary_dir, f"rerun_summary_{timestamp}.txt")
    
    total_rerun = 0
    summary_lines = []
    
    summary_lines.append("=" * 60)
    summary_lines.append(f"重跑清單摘要報告 - {timestamp}")
    summary_lines.append("=" * 60)
    
    for rerun_file in rerun_lists:
        if not rerun_file or not os.path.exists(rerun_file):
            continue
        
        try:
            with open(rerun_file, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                count = sum(1 for _ in reader)
                total_rerun += count
                
                summary_lines.append(f"\n{os.path.basename(rerun_file)}:")
                summary_lines.append(f"  需要重跑條目: {count} 條")
                
                # 重置文件指針重新讀取
                f.seek(0)
                next(reader)  # 跳過標題行
                
                # 顯示前5條
                preview_lines = []
                for i, row in enumerate(reader):
                    if i >= 5:
                        preview_lines.append(f"    還有 {count - 5} 條...")
                        break
                    preview_lines.append(f"    {i+1}. {row.get('法規', '')}{row.get('條號', '')} - {row.get('_quality_issues', '')[:50]}...")
                
                if preview_lines:
                    summary_lines.extend(preview_lines)
                    
        except Exception as e:
            summary_lines.append(f"\n{os.path.basename(rerun_file)}: 讀取失敗 - {e}")
    
    summary_lines.append(f"\n{'='*60}")
    summary_lines.append(f"總計需要重跑: {total_rerun} 條")
    summary_lines.append("=" * 60)
    
    try:
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(summary_lines))
        
        logger.info(f"重跑摘要報告: {summary_path}")
        return summary_path
    except Exception as e:
        logger.error(f"寫入摘要報告失敗: {e}")
        return None

def main():
    """主函數：處理命令行參數"""
    if len(sys.argv) < 3:
        print("用法: python3 generate_rerun_list.py <輸出目錄> <批次名稱>")
        print("示例: python3 generate_rerun_list.py /path/to/output 刑法批次")
        sys.exit(1)
    
    output_dir = sys.argv[1]
    batch_name = sys.argv[2]
    
    if not os.path.exists(output_dir):
        logger.error(f"輸出目錄不存在: {output_dir}")
        sys.exit(1)
    
    # 找到最新的輸出CSV
    latest_csv = find_latest_csv(output_dir)
    if not latest_csv:
        logger.error(f"在目錄中找不到CSV文件: {output_dir}")
        sys.exit(1)
    
    logger.info(f"找到最新輸出文件: {latest_csv}")
    
    # 生成重跑清單
    rerun_list = generate_rerun_list(latest_csv, output_dir, batch_name)
    
    if rerun_list:
        # 生成摘要報告
        summary_dir = os.path.join(os.path.dirname(output_dir), "..", "重跑清單")
        os.makedirs(summary_dir, exist_ok=True)
        
        generate_rerun_summary([rerun_list], summary_dir)
        print(f"✓ 重跑清單已生成: {rerun_list}")
    else:
        print("✓ 沒有需要重跑的條目")

if __name__ == "__main__":
    main()