def test_health(client):
    assert client.get("/health").json()["status"] == "ok"

def test_create_interview(client):
    payload = {
        "participant": "P1", "segment": "enterprise",
        "transcript": "Я хочу быстрее. Мне нужно меньше кликов.",
    }
    r = client.post("/api/interviews", json=payload)
    assert r.status_code == 201
    assert r.json()["participant"] == "P1"

def test_list_insights(client):
    r = client.get("/api/insights")
    assert r.status_code == 200
