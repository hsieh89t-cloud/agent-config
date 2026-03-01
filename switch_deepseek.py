#!/usr/bin/env python3
from pathlib import Path
import json
import os
import sys

WORKSPACE = Path("/home/hsieh89t/.openclaw/workspace")
CONFIG_OUT = WORKSPACE / "config" / "deepseek_config.json"

MODELS = {
    "1": {"label": "DeepSeek Chat", "name": "deepseek-chat", "endpoint": "https://api.deepseek.com/chat/completions"},
    "2": {"label": "DeepSeek Coder", "name": "deepseek-coder", "endpoint": "https://api.deepseek.com/v1/coder"}
}

def mask_key(key: str) -> str:
    if not key:
        return "<未設定>"
    if len(key) <= 8:
        return key[:2] + "***" + key[-2:]
    return key[:4] + "***" + key[-4:]


def pick_model():
    while True:
        print("選擇模型：")
        for idx, meta in MODELS.items():
            print(f"  {idx}. {meta['label']} ({meta['name']})")
        choice = input("輸入選項 (1/2)：").strip()
        if choice in MODELS:
            return MODELS[choice]
        print("無效選項，請重新輸入。\n")


def prompt_api_key(default_key: str) -> str:
    print("目前 API key：", mask_key(default_key))
    new_key = input("若需更換，輸入新 key（直接 Enter 表示沿用）：").strip()
    if new_key:
        return new_key
    return default_key


def write_config(model_meta, api_key):
    data = {
        "model": model_meta["name"],
        "endpoint": model_meta["endpoint"],
        "headers": {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    }
    CONFIG_OUT.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_OUT.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(f"\n已將設定寫入: {CONFIG_OUT}")
    print("可用以下命令檢視內容：")
    print(f"  cat {CONFIG_OUT}")


def main():
    print("=== DeepSeek 模型切換器 ===\n")
    env_key = os.environ.get("DEEPSEEK_API_KEY", "")
    api_key = prompt_api_key(env_key)
    if not api_key:
        print("未提供 API key，無法繼續。")
        sys.exit(1)

    model_meta = pick_model()
    write_config(model_meta, api_key)

    print("\n目前模型：", model_meta["name"])
    print("API key：", mask_key(api_key))
    print("設定已完成，可將輸出的 JSON 套用到請求流程。")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n已取消。")
        sys.exit(130)
