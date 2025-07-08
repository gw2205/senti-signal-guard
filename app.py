from fastapi import FastAPI
from fastapi.responses import JSONResponse
import asyncio
import json
from pathlib import Path
from datetime import datetime

app = FastAPI()
DATA_DIR = Path(__file__).parent / "data"

@app.get("/health")
async def health_check():
    return {"status": "ok", "time": datetime.utcnow().isoformat()}

@app.get("/metrics")
async def metrics():
    fn = DATA_DIR / "status_log.json"
    logs = json.load(fn.open()) if fn.exists() else []
    return JSONResponse(content={"logs": logs})
