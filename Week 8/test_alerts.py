from fastapi.testclient import TestClient
from requests.auth import HTTPBasicAuth

import app

client = TestClient(app.app)

auth = HTTPBasicAuth('admin', 'password123')
bad_auth = HTTPBasicAuth('admin', 'badpassword')

# Test Unauthorized line
def test_read_main_alerts_unauthorized_nologin():
    response = client.get("/alerts")
    assert response.status_code == 401 # Check for unauthorized status code

# Test unauthorized route
def test_read_main_alerts_unauthorized_bad_credentials():
    response = client.get("/alerts", auth=bad_auth)
    assert response.status_code == 401 # Check for unauthorized status code

def test_read_main_alerts_authorized():
    response = client.get("/alerts", auth=auth)
    assert response.status_code == 200 # Check for authorized status code