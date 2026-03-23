from fastapi.testclient import TestClient
from requests.auth import HTTPBasicAuth

import app

client = TestClient(app.app)

auth = HTTPBasicAuth('admin', 'password123')
bad_auth = HTTPBasicAuth('admin', 'badpassword')

# Test Unauthorized line
def test_read_main_vehicle_unauthorized_nologin():
    response = client.get("/vehicles")
    assert response.status_code == 401 # Check for unauthorized status code

# Test unauthorized route
def test_read_main_vehicle_unauthorized_bad_credentials():
    response = client.get("/vehicles", auth=bad_auth)
    assert response.status_code == 401 # Check for unauthorized status code

def test_read_main_vehicle_authorized():
    response = client.get("/vehicles", auth=auth)
    assert response.status_code == 200 # Check for authorized status code

def test_read_vehicle_content():
    response = client.get("/vehicles/y1604", auth=auth)
    print(response.json()) # Fetch route details from json response
    assert response.status_code == 200 # Check status code is 200 ok
    vehicle = response.json().get("vehicle")
    # Verify route details
    assert vehicle.get("id") == "y1604"
    assert vehicle.get("updated_at") is not None
    assert vehicle.get("current_status") is not None

def test_read_vehicle_not_found():
    vehicle_id = "Chauncey"
    response = client.get(f"/vehicles/{vehicle_id}", auth=auth)
    assert response.status_code == 404
    print(response.json())
    assert response.json().get("message") == f"vehicle with id {vehicle_id} not found"