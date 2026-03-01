#!/usr/bin/env python3
import json
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

STATE_PATH = Path("ai_agent_state.json")
LOG_PATH = Path("ai_agent_updates.log")
DIGEST_PATH = Path("ai_agent_digest.md")
QUERY = "AI agent"
API_URL = "https://hn.algolia.com/api/v1/search_by_date"
FETCH_PARAMS = {
    "query": QUERY,
    "tags": "story",
    "numericFilters": "created_at_i>1740787200"
}
FETCH_INTERVAL = 30  # seconds


def fetch_items():
    params = urllib.parse.urlencode(FETCH_PARAMS)
    url = f"{API_URL}?{params}"
    with urllib.request.urlopen(url, timeout=15) as resp:
        data = json.load(resp)
    hits = data.get("hits", [])
    items = []
    for h in hits:
        title = h.get("title") or h.get("story_title")
        if not title:
            continue
        items.append({
            "objectID": h.get("objectID"),
            "title": title,
            "url": h.get("url") or h.get("story_url"),
            "created_at": h.get("created_at"),
            "author": h.get("author"),
            "story_text": h.get("story_text")
        })
    return items


def load_state():
    if STATE_PATH.exists():
        with STATE_PATH.open() as f:
            return set(json.load(f).get("seen_ids", []))
    return set()


def save_state(seen_ids):
    with STATE_PATH.open("w") as f:
        json.dump({"seen_ids": sorted(seen_ids)}, f, indent=2)


def log(message):
    timestamp = datetime.now(timezone.utc).isoformat()
    with LOG_PATH.open("a") as f:
        f.write(f"[{timestamp}] {message}\n")


def append_digest(item):
    snippet = (item.get("story_text") or "").replace("\n", " ")
    snippet = snippet[:240] + ("…" if len(snippet) > 240 else "")
    with DIGEST_PATH.open("a") as f:
        f.write(
            f"\n### Update {datetime.now(timezone.utc).isoformat()}\n"
            f"- **Title:** {item['title']}\n"
            f"- **Link:** {item.get('url') or 'HN discussion'}\n"
            f"- **Author:** {item.get('author') or 'unknown'}\n"
            f"- **Summary hint:** {snippet or 'N/A'}\n"
        )


def main_loop():
    seen_ids = load_state()
    log(f"Monitor loop started. Tracking {len(seen_ids)} existing items.")
    while True:
        try:
            items = fetch_items()
            new_items = [i for i in items if i.get("objectID") and i["objectID"] not in seen_ids]
            if new_items:
                for item in new_items:
                    seen_ids.add(item["objectID"])
                    log(f"New item: {item['title']} ({item.get('url') or 'HN discussion'})")
                    append_digest(item)
                save_state(seen_ids)
            else:
                log("No new items detected this cycle.")
        except Exception as exc:
            log(f"Error during fetch: {exc}")
        time.sleep(FETCH_INTERVAL)


if __name__ == "__main__":
    main_loop()
