#!/usr/bin/env python3
import os
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from telegram import Update, Bot
from telegram.error import TelegramError
from telegram_bot import send_message

load_dotenv()
TOKEN       = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID     = os.getenv("TELEGRAM_CHAT_ID")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

if not (TOKEN and CHAT_ID and WEBHOOK_URL):
    raise RuntimeError("Set TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID & WEBHOOK_URL")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S"
)
log = logging.getLogger("sentibot")

bot = Bot(token=TOKEN)
app = FastAPI()

class UpdateIn(BaseModel):
    update_id: int
    message: dict | None           = None
    callback_query: dict | None    = None

@app.on_event("startup")
async def on_startup():
    try:
        await bot.set_webhook(WEBHOOK_URL)
        log.info(f"✅ Webhook set → {WEBHOOK_URL}")
    except TelegramError as err:
        log.error(f"❌ set_webhook failed: {err}")
        raise

@app.post("/webhook")
async def webhook(update_in: UpdateIn):
    upd = Update.de_json(update_in.dict(), bot)
    log.info(f"📬 update_id={upd.update_id}")
    try:
        await handle_update(upd)
    except Exception:
        log.exception("💥 handle_update error")
        raise HTTPException(500, "Internal Error")
    return {"ok": True}

async def handle_update(upd: Update):
    msg = upd.message
    if not (msg and msg.text):
        return

    text = msg.text.lower()
    log.info(f"✉️ chat={msg.chat.id} text={text!r}")
    if "score:" in text:
        try:
            score = float(text.split("score:")[1].strip().rstrip("%"))
        except ValueError:
            return
        if score > 70:
            alert = f"🔥 *UNKNOWN* sentiment score: {score:.1f}%"
            log.info(f"🚀 send alert to chat={CHAT_ID}")
            resp = send_message(alert)
            log.info(f"✅ telegram response: {resp}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
