# sentibot/utils/source_manager.py
import os, json, asyncio, logging
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

# ---------- הגדרות בסיס ----------
load_dotenv()                                      # קורא משתני env מריילווי
DATA_DIR = Path(__file__).resolve().parents[1] / "data"
TIMEOUT = ClientTimeout(total=8)
logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger("SourceManager")

# ---------- עזרי JSON ----------
def load_json(fname):
    with open(DATA_DIR / fname, encoding="utf-8") as f:
        return json.load(f)

def save_json(fname, data):
    with open(DATA_DIR / fname, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ---------- חיבורי API ----------
telegram_client = TelegramClient(
    os.getenv("TG_SESSION", "sentibot"),
    int(os.getenv("TG_API_ID")),
    os.getenv("TG_API_HASH")
)

twitter_client = tweepy.Client(os.getenv("TW_BEARER_TOKEN"), wait_on_rate_limit=True)
yt_service      = buil_
