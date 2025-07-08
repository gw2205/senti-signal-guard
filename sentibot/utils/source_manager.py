# sentibot/utils/source_manager.py

import os
import json
import asyncio
import logging
from pathlib import Path
from datetime import datetime

import aiohttp
from aiohttp import ClientTimeout
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.errors import UsernameInvalidError, ChannelInvalidError
import tweepy
from googleapiclient.discovery import build
from tiktokapipy.async_api import TikTokApi

# Basic configuration
load_dotenv()
DATA_DIR = Path(__file__).resolve().parents[1] / "data"
TIMEOUT = ClientTimeout(total=8)
logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger("SourceManager")

# JSON helpers
def load_json(fname):
    with open(DATA_DIR / fname, encoding="utf-8") as f:
        return json.load(f)

def save_json(fname, data):
    with open(DATA_DIR / fname, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# API clients
telegram_client = TelegramClient(
    os.getenv("TG_SESSION", "sentibot"),
    int(os.getenv("TG_API_ID")),
    os.getenv("TG_API_HASH")
)
twitter_client = tweepy.Client(os.getenv("TW_BEARER_TOKEN"), wait_on_rate_limit=True)
yt_service      = build("youtube", "v3", developerKey=os.getenv("YT_API_KEY"))
tiktok_client   = TikTokApi(timeout=TIMEOUT)

async def fetch_tokens():
    # replace the following with your existing token-gathering logic
    tokens = []
    # ... populate tokens list ...

    # filter and print only tokens with score > 70
    for tok in tokens:
        if tok.score > 70:
            print(f"{tok.symbol}: {tok.score}")

    return tokens

if __name__ == "__main__":
    asyncio.run(fetch_tokens())
