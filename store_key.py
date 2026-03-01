#!/usr/bin/env python3
"""Interactive helper to register API keys or tokens safely into config/keys."""
from __future__ import annotations

import getpass
import json
from datetime import datetime, timezone
from pathlib import Path
import sys

WORKDIR = Path("/home/hsieh89t/.openclaw/workspace")
KEY_DIR = WORKDIR / "config" / "keys"
KEY_DIR.mkdir(parents=True, exist_ok=True)
KEY_FILE = KEY_DIR / "secure_keys.json"


def load_keys() -> dict:
    if KEY_FILE.exists():
        try:
            return json.loads(KEY_FILE.read_text())
        except json.JSONDecodeError:
            print("[警告] secure_keys.json 內容毀損，將重新建立空白檔。")
    return {}


def save_keys(data: dict) -> None:
    KEY_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False))


def mask(value: str) -> str:
    if len(value) <= 6:
        return value[:1] + "***"
    return value[:4] + "***" + value[-4:]


def main() -> None:
    print("=== API Key 儲存助手 ===")
    label = input("請輸入此 key 的名稱（例如 deepseek_bot）：").strip()
    if not label:
        print("未輸入名稱，中止。")
        sys.exit(1)

    existing = load_keys()
    if label in existing:
        print(f"[資訊] 現有值：{mask(existing[label]['value'])}")
        overwrite = input("要覆寫嗎？(y/N)：").strip().lower()
        if overwrite != "y":
            print("已取消。")
            sys.exit(0)

    first = getpass.getpass("請輸入 API key：")
    if not first:
        print("未輸入 key，中止。")
        sys.exit(1)
    second = getpass.getpass("再輸入一次確認：")
    if first != second:
        print("兩次輸入不一致，中止。")
        sys.exit(1)

    note = input("備註（可留空）：").strip()

    existing[label] = {
        "value": first,
        "note": note,
        "updated_at": datetime.now(timezone.utc).isoformat()
    }
    save_keys(existing)

    print("\n已儲存。摘要：")
    print(f"- 名稱：{label}")
    print(f"- Key：{mask(first)}")
    if note:
        print(f"- 備註：{note}")
    print(f"- 存檔：{KEY_FILE}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n已取消。")
        sys.exit(130)
