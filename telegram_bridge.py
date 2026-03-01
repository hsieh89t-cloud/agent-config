#!/usr/bin/env python3
"""Simple Telegram polling bridge to capture user messages for manual responses."""

from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict
import urllib.request
import urllib.parse

WORKDIR = Path("/home/hsieh89t/.openclaw/workspace")
KEY_FILE = WORKDIR / "config" / "keys" / "secure_keys.json"
STATE_FILE = WORKDIR / "config" / "bot_bridge_state.json"
INBOX_LOG = WORKDIR / "telegram_inbox.log"
ALLOWED_CHAT_ID = 8236290134
TOKEN_LABEL = "@ysga168bot"
POLL_TIMEOUT = 25
SLEEP_BETWEEN = 2


def load_token() -> str:
    if not KEY_FILE.exists():
        raise SystemExit(f"Key file not found: {KEY_FILE}")
    data = json.loads(KEY_FILE.read_text())
    entry = data.get(TOKEN_LABEL)
    if not entry or not entry.get("value"):
        raise SystemExit(f"Key '{TOKEN_LABEL}' missing in {KEY_FILE}")
    return entry["value"].strip()


def load_state() -> int:
    if STATE_FILE.exists():
        try:
            data = json.loads(STATE_FILE.read_text())
            return int(data.get("last_update_id", 0))
        except json.JSONDecodeError:
            pass
    return 0


def save_state(update_id: int) -> None:
    STATE_FILE.write_text(json.dumps({"last_update_id": update_id}, indent=2))


def call_telegram(token: str, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
    base = f"https://api.telegram.org/bot{token}/{method}"
    if params:
        query = urllib.parse.urlencode(params)
        url = f"{base}?{query}"
    else:
        url = base
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=POLL_TIMEOUT + 5) as resp:
        return json.load(resp)


def append_log(entry: str) -> None:
    timestamp = datetime.now(timezone.utc).isoformat()
    INBOX_LOG.parent.mkdir(parents=True, exist_ok=True)
    with INBOX_LOG.open("a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {entry}\n")


def handle_message(msg: Dict[str, Any]) -> None:
    chat = msg.get("chat", {})
    chat_id = chat.get("id")
    text = msg.get("text")
    if chat_id != ALLOWED_CHAT_ID:
        append_log(f"Ignored message from chat {chat_id}: {text}")
        return
    user = chat.get("first_name") or chat.get("username") or chat_id
    entry = f"{user}: {text}"
    print(entry)
    append_log(entry)


def main() -> None:
    token = load_token()
    last_update_id = load_state()
    print("=== Telegram Bridge Started ===")
    print(f"Tracking chat ID: {ALLOWED_CHAT_ID}")
    while True:
        params = {
            "offset": last_update_id + 1,
            "timeout": POLL_TIMEOUT
        }
        try:
            data = call_telegram(token, "getUpdates", params)
        except Exception as exc:  # pylint: disable=broad-except
            append_log(f"[error] {exc}")
            time.sleep(SLEEP_BETWEEN)
            continue

        if not data.get("ok"):
            append_log(f"[error] Telegram response not ok: {data}")
            time.sleep(SLEEP_BETWEEN)
            continue

        updates = data.get("result", [])
        if not updates:
            continue

        for update in updates:
            update_id = update.get("update_id", last_update_id)
            last_update_id = max(last_update_id, update_id)
            message = update.get("message") or update.get("edited_message")
            if message:
                handle_message(message)
        save_state(last_update_id)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nBridge stopped by user.")
