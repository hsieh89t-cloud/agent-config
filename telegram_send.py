#!/usr/bin/env python3
"""Send a manual Telegram message via the configured bot."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import urllib.request
import urllib.parse

WORKDIR = Path("/home/hsieh89t/.openclaw/workspace")
KEY_FILE = WORKDIR / "config" / "keys" / "secure_keys.json"
DEFAULT_CHAT_ID = 8236290134
TOKEN_LABEL = "@ysga168bot"


def load_token() -> str:
    if not KEY_FILE.exists():
        raise SystemExit(f"Key file not found: {KEY_FILE}")
    data = json.loads(KEY_FILE.read_text())
    entry = data.get(TOKEN_LABEL)
    if not entry or not entry.get("value"):
        raise SystemExit(f"Key '{TOKEN_LABEL}' missing in {KEY_FILE}")
    return entry["value"].strip()


def send_message(token: str, chat_id: int, text: str) -> None:
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    data = urllib.parse.urlencode(payload).encode()
    req = urllib.request.Request(url, data=data)
    with urllib.request.urlopen(req, timeout=30) as resp:
        response = json.load(resp)
    if not response.get("ok"):
        raise SystemExit(f"Telegram API error: {response}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Send Telegram message via local bot")
    parser.add_argument("text", help="訊息內容")
    parser.add_argument("--chat-id", type=int, default=DEFAULT_CHAT_ID, help="目標 chat id")
    args = parser.parse_args()

    token = load_token()
    send_message(token, args.chat_id, args.text)
    print("已送出。")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n已取消。")
        sys.exit(130)
