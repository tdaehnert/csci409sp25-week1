from fastapi import FastAPI, Depends
import requests, httpx

API_KEY = "c0be3e73b2f542a296dccaa25dedea7a" # Fill in with your API Key
ENDPOINT_URL = "https://api-v3.mbta.com/" # DO NOT CHANGE THIS


app = FastAPI() # Initialize the end point

@app.get("/") # Create a default route
def read_root():
    return {"message": "Vehicle Information Microservice Running!"}

# Get a list of all vehicles
@app.get("/vehicles")
def get_vehicles(route: str = None, revenue: str = None):
    params = {}
    if route:
        params["filter[route]"] = route
    if revenue:
        params["filter[revenue]"] = revenue

    response = requests.get(f"{ENDPOINT_URL}/vehicles", params=params)
    response.raise_for_status()
    return response.json()


    # Get information on a specific vehicle
@app.get("/vehicles/{vehicle_id}")
def get_vehicle(vehicle_id: str):
    response = requests.get(f"{ENDPOINT_URL}/vehicles/{vehicle_id}?api_key={API_KEY}")  # Send a request to the endpoint
    response.raise_for_status()
    return response.json()

# Dependency to fetch all alerts
async def get_all_alerts(route: str = None, stop: str = None):
        params = {}
        if route:
            params["filter[route]"] = route
        if stop:
            params["filter[stop]"] = stop

        async with httpx.AsyncClient() as client:
            response = await client.get(f"{ENDPOINT_URL}/alerts", params=params)
            response.raise_for_status()
            return response.json()

# Dependency to fetch a specific alert by ID
async def get_alert_by_id(alert_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{ENDPOINT_URL}/alerts/{alert_id}?api_key={API_KEY}")
        response.raise_for_status()
        return response.json()


@app.get("/alerts")
async def read_alerts(route: str = None, stop: str = None, alerts=Depends(get_all_alerts)):
    return alerts

@app.get("/alerts/{alert_id}")
async def read_alert(alert_id: str, alert=Depends(get_alert_by_id)):
    return alert