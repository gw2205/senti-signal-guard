# sentiment_scoring.py
import re
from ..data.keywords_positive import POSITIVE_KEYWORDS
from ..data.keywords_negative import NEGATIVE_KEYWORDS

def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text

def compute_sentiment_score(messages):
    total_score = 0
    total_count = 0

    for msg in messages:
        text = preprocess(msg)
        score = 0

        for word in POSITIVE_KEYWORDS:
            if word in text:
                score += 1
        for word in NEGATIVE_KEYWORDS:
            if word in text:
                score -= 1

        total_score += score
        total_count += 1

    if total_count == 0:
        return 0

    return round(total_score / total_count, 2)
