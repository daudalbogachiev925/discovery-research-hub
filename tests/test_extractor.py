from app.nlp.extractor import split_insights, to_jtbd

def test_split_insights_markers():
    text = "Я хочу быстрее. Мне нужно меньше кликов. Просто текст."
    insights = split_insights(text)
    assert len(insights) >= 2

def test_split_insights_fallback():
    text = "Просто предложение без маркеров. Ещё одно."
    assert len(split_insights(text)) >= 1

def test_jtbd_keys():
    result = to_jtbd(["Хочу быстрее", "Нужна интеграция"])
    assert "situation" in result
    assert "motivation" in result
    assert "outcome" in result
