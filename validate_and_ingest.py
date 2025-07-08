#!/usr/bin/env python3
import os
import json
import asyncio
import logging
from pathlib import Path
from datetime import datetime
import aiohttp
from aiohttp import ClientTimeout
from dotenv import load_dotenv

# ←––– Basic config –––→
load_dotenv()
DATA_DIR = Path(__file__).parent / "data"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
logging.basicConfig(level=LOG_LEVEL, format="%(message)s")
log = logging.getLogger("ingest")

# ←––– Ping one source –––→
async def ping(name: str, url: str) -> tuple[str, bool]:
    try:
        async with aiohttp.ClientSession(timeout=ClientTimeout(total=5)) as session:
            async with session.head(url) as resp:
                return name, resp.status < 400
    except:
        return name, False

# ←––– Load all sources from JSON files –––→
def load_sources() -> dict[str, str]:
    out = {}
    for cat in ("twitter", "telegram", "reddit", "youtube", "tiktok"):
        path = DATA_DIR / f"{cat}_sources.json"
        if path.exists():
            for entry in json.loads(path.read_text()):
                out[entry["name"]] = entry["url"]
    return out

# ←––– Append status to the log file –––→
def record_status(results: list[tuple[str, bool]]):
    path = DATA_DIR / "status_log.json"
    old = json.loads(path.read_text()) if path.exists() else []
    new = [
        {"time": datetime.utcnow().isoformat(), "source": n, "alive": a}
        for n, a in results
    ]
    path.write_text(json.dumps(old + new, indent=2))

# ←––– Main flow –––→
async def main():
    sources = load_sources()
    results = await asyncio.gather(*(ping(n, u) for n, u in sources.items()))
    for name, alive in results:
        log.info(f"{name}: {'✅' if alive else '❌'}")
    record_status(results)

if __name__ == "__main__":
    asyncio.run(main())
