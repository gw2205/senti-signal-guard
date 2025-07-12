# data_parser.py
import os
import json

DATA_FOLDER = "data"

def load_sources_and_messages():
    results = []

    for filename in os.listdir(DATA_FOLDER):
        if not filename.endswith(".json"):
            continue

        filepath = os.path.join(DATA_FOLDER, filename)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"Failed to read {filepath}: {e}")
            continue

        for entry in data:
            token = entry.get("token")
            messages = entry.get("messages", [])
            source_type = entry.get("source_type", filename.replace(".json", ""))

            if token and messages:
                results.append({
                    "token": token,
                    "messages": messages,
                    "source_type": source_type
                })

    return results
