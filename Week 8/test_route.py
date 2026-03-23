from fastapi.testclient import TestClient
from requests.auth import HTTPBasicAuth

import app

client = TestClient(app.app)

auth = HTTPBasicAuth('admin', 'password123')
bad_auth = HTTPBasicAuth('admin', 'badpassword')

# Test Unauthorized route
def test_read_main_route_unauthorized_nologin():
    response = client.get("/routes")
    assert response.status_code == 401 # Check for unauthorized status code

# Test unauthorized route
def test_read_main_route_unauthorized_bad_credentials():
    response = client.get("/routes", auth=bad_auth)
    assert response.status_code == 401 # Check for unauthorized status code

def test_read_main_route_authorized():
    response = client.get("/routes", auth=auth)
    assert response.status_code == 200 # Check for authorized status code

def test_read_route_content():
    response = client.get("/routes/Red", auth=auth)
    route = response.json().get("route") # Fetch route details from json response
    assert response.status_code == 200 # Check status code is 200 ok
    # Verify route details
    assert route.get("id") == 'Red'
    assert route.get("type") == 1
    assert route.get("color") == 'DA291C'
    assert route.get("text_color") == 'FFFFFF'
    assert route.get("description") == 'Rapid Transit'
    assert route.get("long_name") == 'Red Line'

def test_read_route_not_found():
    route_id = "Chauncey"
    response = client.get(f"/routes/{route_id}", auth=auth)
    assert response.status_code == 404
    print(response.json())
    assert response.json().get("message") == f"Route with id {route_id} not found"