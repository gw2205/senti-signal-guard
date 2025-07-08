#!/usr/bin/env python3
import asyncio
import json
import logging
from pathlib import Path
from datetime import datetime

# ——— Config ———
DATA_DIR = Path(__file__).parent / "data"
STATUS_FILE = DATA_DIR / "status_log.json"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)
logger = logging.getLogger("validate_and_ingest")

# ——— Your existing imports & helpers ———
# import ... (כל מה שיש לך כרגע)
# לדוגמה:
# from sentibot.utils.source_manager import fetch_all_data

# ——— Record status to disk ———
def record_status(results: list[dict]):
    logger.info(f"📝 Preparing to write {len(results)} results to `{STATUS_FILE}`")
    # ודא שתיקיית הנתונים קיימת
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # קרא קודם־כל היסטוריה
    old = []
    if STATUS_FILE.exists():
        text = STATUS_FILE.read_text(encoding="utf-8")
        old = json.loads(text)
        logger.info(f"🔄 Loaded {len(old)} previous entries")

    # הוסף רשומה חדשה
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "results": results,
    }
    combined = old + [entry]

    # כתיבה חזרה
    STATUS_FILE.write_text(json.dumps(combined, indent=2, ensure_ascii=False), encoding="utf-8")
    logger.info("✅ Successfully wrote status_log.json")


# ——— Main flow ———
async def main():
    logger.info("🚀 Starting main()")
    # כאן תקרא לפונקציית האיסוף/וולידציה שלך
    # למשל: results = await fetch_all_data()
    # ----- Example placeholder -----
    # דוגמא מדומה – החלף בלוגיקה שלך!
    results = [{"dummy": "data"}]
    logger.info(f"🔍 Collected {len(results)} items")
    # --------------------------------

    record_status(results)
    logger.info("🏁 main() completed")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logger.exception("❌ Unhandled exception in main()")
        raise
