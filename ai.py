import json
import os
import urllib.error
import urllib.request

MODEL = "cardiffnlp/twitter-xlm-roberta-base-sentiment"
API_URL = "https://router.huggingface.co/hf-inference/models/" + MODEL

LABELS = {
    "positive": "позитивний",
    "neutral": "нейтральний",
    "negative": "негативний",
}


def parse_sentiment(response):
    candidates = response[0] if response and isinstance(response[0], list) else response
    best = max(candidates, key=lambda item: item["score"])
    return best["label"].lower(), round(float(best["score"]), 4)


def analyze_sentiment(text, token=None):
    token = token or os.environ.get("HF_TOKEN")
    if not token:
        return None, None
    payload = json.dumps({"inputs": text}).encode("utf-8")
    request = urllib.request.Request(
        API_URL,
        data=payload,
        headers={
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            data = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, ValueError, KeyError, IndexError):
        return None, None
    return parse_sentiment(data)


def label_uk(label):
    return LABELS.get(label, "не визначено")
