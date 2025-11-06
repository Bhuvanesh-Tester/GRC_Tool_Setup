from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    res = client.get("/")
    assert res.status_code == 200
    assert "GRC Platform API" in res.json().get("message", "")

def test_demo_login_and_me():
    res = client.post("/api/v1/auth/login", json={"role": "admin"})
    assert res.status_code == 200
    token = res.json()["access_token"]
    res2 = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert res2.status_code == 200
    assert res2.json()["role"] == "admin"