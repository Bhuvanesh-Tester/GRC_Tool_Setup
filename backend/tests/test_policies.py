from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def get_admin_token():
    res = client.post("/api/v1/auth/login", json={"role": "admin"})
    return res.json()["access_token"]

def test_list_policies():
    token = get_admin_token()
    res = client.get("/api/v1/policies/", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    data = res.json()
    assert "items" in data and data["total"] >= 1

def test_create_update_delete_policy():
    token = get_admin_token()
    # create
    res = client.post("/api/v1/policies/", json={"title": "Access Control", "description": "AC policy"}, headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    pid = res.json()["id"]
    # update
    res2 = client.put(f"/api/v1/policies/{pid}", json={"status": "Approved"}, headers={"Authorization": f"Bearer {token}"})
    assert res2.status_code == 200
    assert res2.json()["status"] == "Approved"
    # delete
    res3 = client.delete(f"/api/v1/policies/{pid}", headers={"Authorization": f"Bearer {token}"})
    assert res3.status_code == 200