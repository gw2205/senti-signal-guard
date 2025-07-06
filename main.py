# FastAPI server to run SignalBot and SentiBot

from fastapi import FastAPI
from signalbot import run_signal
from sentibot import run_sentiment_scan

app = FastAPI()

@app.get("/run_signal")
def trigger_signal(symbol: str):
    return run_signal(symbol)

@app.get("/scan_sentiment")
def trigger_sentiment():
    return run_sentiment_scan()

@app.get("/status")
def status():
    return {"status": "running"}