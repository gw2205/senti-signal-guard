# sentibot_engine.py
import json
from .sentiment_scoring import compute_sentiment_score
from .data_parser import load_sources_and_messages

def run_sentiment_engine():
    results = []

    # טען את כל המקורות
    all_sources = load_sources_and_messages()

    for item in all_sources:
        source_type = item.get("source_type")
        token = item.get("token")
        messages = item.get("messages")

        if not token or not messages:
            continue

        score = compute_sentiment_score(messages)

        results.append({
            "token": token,
            "score": score,
            "source": source_type,
            "messages_analyzed": len(messages)
        })

    return results

if __name__ == "__main__":
    sentiment_data = run_sentiment_engine()
    print(json.dumps(sentiment_data, indent=2))
