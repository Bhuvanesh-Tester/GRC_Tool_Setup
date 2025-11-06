from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def get_manager_token():
    res = client.post("/api/v1/auth/login", json={"role": "risk_manager"})
    return res.json()["access_token"]

def test_create_risk_and_score():
    token = get_manager_token()
    res = client.post("/api/v1/risks/", json={"title": "Server Outage", "impact": 4, "likelihood": 2}, headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    data = res.json()
    assert data["score"] == 8