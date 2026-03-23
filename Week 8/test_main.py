from fastapi.testclient import TestClient

import app

client = TestClient(app.app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json().get("message") == "Welcome to my FastAPI Application!"