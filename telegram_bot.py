#!/usr/bin/env python3
import os
import requests
import logging

# simple wrapper around Telegram sendMessage API
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("telegram_bot")

def send_message(msg: str) -> dict:
    token  = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    url    = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id":    chat_id,
        "text":       msg,
        "parse_mode": "Markdown"
    }

    log.info(f"→ POST {url} payload={payload!r}")
    resp = requests.post(url, data=payload)
    try:
        body = resp.json()
    except ValueError:
        log.error("Invalid JSON in Telegram response", resp.text)
        raise

    log.info("← Telegram replied %s", body)
    return body
