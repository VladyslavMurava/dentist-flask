import ai


def test_parse_sentiment_nested_list():
    response = [[
        {"label": "positive", "score": 0.89},
        {"label": "neutral", "score": 0.08},
        {"label": "negative", "score": 0.03},
    ]]
    assert ai.parse_sentiment(response) == ("positive", 0.89)


def test_parse_sentiment_flat_list():
    response = [
        {"label": "Negative", "score": 0.7},
        {"label": "Positive", "score": 0.3},
    ]
    assert ai.parse_sentiment(response) == ("negative", 0.7)


def test_label_uk_known_and_unknown():
    assert ai.label_uk("positive") == "позитивний"
    assert ai.label_uk("negative") == "негативний"
    assert ai.label_uk(None) == "не визначено"


def test_analyze_without_token_returns_none(monkeypatch):
    monkeypatch.delenv("HF_TOKEN", raising=False)
    assert ai.analyze_sentiment("будь-який текст") == (None, None)
