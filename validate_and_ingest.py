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
STATUS_FILE = DATA_DIR / "status_log.json"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S"
)
log = logging.getLogger("ingest")

# ←––– Ping one source –––→
async def ping(name: str, url: str) -> tuple[str, bool]:
    try:
        async with aiohttp.ClientSession(timeout=ClientTimeout(total=5)) as session:
            async with session.head(url) as resp:
                return name, resp.status < 400
    except Exception as e:
        log.debug(f"ping error for {name}: {e}")
        return name, False

# ←––– Load all sources from JSON files –––→
def load_sources() -> dict[str, str]:
    sources = {}
    for cat in ("twitter", "telegram", "reddit", "youtube", "tiktok"):
        fn = DATA_DIR / f"{cat}_sources.json"
        if fn.exists():
            try:
                entries = json.loads(fn.read_text(encoding="utf-8"))
                for entry in entries:
                    sources[entry["name"]] = entry["url"]
            except Exception as e:
                log.warning(f"failed to load {fn.name}: {e}")
    return sources

# ←––– Append status to the log file –––→
def record_status(results: list[tuple[str, bool]]):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    old = []
    if STATUS_FILE.exists():
        try:
            old = json.loads(STATUS_FILE.read_text(encoding="utf-8"))
        except Exception as e:
            log.warning(f"could not parse existing status file: {e}")

    new = [
        {"time": datetime.utcnow().isoformat(), "source": name, "alive": alive}
        for name, alive in results
    ]
    combined = old + new
    STATUS_FILE.write_text(json.dumps(combined, indent=2), encoding="utf-8")
    log.info(f"Wrote {len(new)} new entries (total {len(combined)}) to {STATUS_FILE}")

# ←––– Main flow –––→
async def main():
    log.info("▶️ Starting validate_and_ingest run")
    sources = load_sources()
    if not sources:
        log.warning("No source files found in data/ → nothing to ping")
        return

    log.info(f"🌐 Loaded {len(sources)} endpoints to ping")
    results = await asyncio.gather(*(ping(n, u) for n, u in sources.items()))

    for name, alive in results:
        status = "✅ OK" if alive else "❌ FAIL"
        log.info(f"🔍 {name:12s} → {status}")

    record_status(results)
    log.info("🏁 Run finished")

if __name__ == "__main__":
    asyncio.run(main())
