#!/usr/bin/env python3
"""Interactively set the DeepSeek API key inside ~/.openclaw/openclaw.json."""
from __future__ import annotations

import json
import os
from pathlib import Path
import sys
import getpass

CONFIG_PATH = Path.home() / ".openclaw" / "openclaw.json"
BACKUP_PATH = CONFIG_PATH.with_suffix(".json.bak")

DEEPSEEK_DEFAULT = {
    "baseUrl": "https://api.deepseek.com/v1",
    "api": "openai-responses",
    "models": [
        {"id": "deepseek-chat", "name": "DeepSeek Chat (V3)"},
        {"id": "deepseek-reasoner", "name": "DeepSeek Reasoner (R1)"},
    ],
}


def load_config() -> dict:
    if not CONFIG_PATH.exists():
        print(f"找不到 {CONFIG_PATH}，請先跑 openclaw onboard", file=sys.stderr)
        sys.exit(1)
    with CONFIG_PATH.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def save_config(data: dict) -> None:
    BACKUP_PATH.write_text(CONFIG_PATH.read_text(encoding="utf-8"), encoding="utf-8")
    with CONFIG_PATH.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print(f"已更新 {CONFIG_PATH}（備份寫到 {BACKUP_PATH}）")


def prompt_key() -> str:
    existing = os.environ.get("DEEPSEEK_API_KEY")
    masked = None
    if existing:
        masked = existing[:4] + "***" + existing[-4:] if len(existing) > 8 else "***"
    print("\n=== DeepSeek API Key 設定 ===")
    if masked:
        print(f"目前 shell 環境變數：{masked}")
    key = getpass.getpass("輸入 DeepSeek API key（不會回顯）：").strip()
    if not key:
        print("未輸入 key，取消。", file=sys.stderr)
        sys.exit(1)
    return key


def main():
    config = load_config()
    key = prompt_key()

    models_cfg = config.setdefault("models", {})
    if models_cfg.get("mode") is None:
        models_cfg["mode"] = "merge"
    providers = models_cfg.setdefault("providers", {})
    deepseek_cfg = providers.setdefault("deepseek", {})

    deepseek_cfg.update(DEEPSEEK_DEFAULT)
    deepseek_cfg["apiKey"] = key

    save_config(config)
    print("DeepSeek API key 已寫入 config。建議同時：")
    print("  1. 將 key 寫入 ~/.openclaw/.env 供 gateway 使用 (可選)。")
    print("  2. 執行 `openclaw models list | grep deepseek` 驗證。")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n已取消。", file=sys.stderr)
        sys.exit(130)
