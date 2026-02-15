from fastapi import FastAPI
import requests

API_KEY = "c0be3e73b2f542a296dccaa25dedea7a" # Fill in with your API Key
ENDPOINT_URL = "https://api-v3.mbta.com/" # DO NOT CHANGE THIS


app = FastAPI() # Initialize the end point

@app.get("/") # Create a default route
def read_root():
    return {"message": "Route Information Microservice Running!"}

# Get a list of all routes
@app.get("/routes")
def get_routes():
    routes_list = list()
    response = requests.get(ENDPOINT_URL+f"/routes?&api_key={API_KEY}") # Send a request to the endpoint
    # Convert the response to json and extract the data key
    routes = response.json()["data"]
    for route in routes:
        # Loop through all routes extracting relevant information
        routes_list.append({
            "id": route["id"],
            "type": route["type"],
            "color": route["attributes"]["color"],
            "text_color": route["attributes"]["text_color"],
            "description": route["attributes"]["description"],
            "long_name": route["attributes"]["long_name"],
            "type": route["attributes"]["type"],
        })
    # Return the routes_list in JSON format
    return {"routes": routes_list}

# Get information on a specific route
@app.get("/routes/{route_id}")
def get_route(route_id: str):
    response = requests.get(ENDPOINT_URL + f"/routes/{route_id}?api_key={API_KEY}") # Send a request to the endpoint
    # Convert the response to json and extract the data key
    route_data = response.json()["data"]
    # Extract the relevant data
    route = {
        "id": route_data["id"],
        "type": route_data["type"],
        "color": route_data["attributes"]["color"],
        "text_color": route_data["attributes"]["text_color"],
        "description": route_data["attributes"]["description"],
        "long_name": route_data["attributes"]["long_name"],
        "type": route_data["attributes"]["type"],
    }
    # Return the data to the user
    return {"routes": route}

@app.get("/lines")
def get_lines():
    lines_list = list()
    response = requests.get(ENDPOINT_URL + f"/lines?&api_key={API_KEY}")  # Send a request to the endpoint
    # Convert the response to json and extract the data key
    lines = response.json()["data"]
    for line in lines:
        # Loop through all routes extracting relevant information
        lines_list.append({
            "id": line["id"],
            "text_color": line["attributes"]["text_color"],
            "short_name": line["attributes"]["short_name"],
            "long_name": line["attributes"]["long_name"],
            "color": line["attributes"]["color"],
        })
    # Return the lines_list in JSON format
    return {"lines": lines_list}

    # Get information on a specific line
@app.get("/lines/{line_id}")
def get_lines(line_id: str):
    response = requests.get(
        ENDPOINT_URL + f"/lines/{line_id}?api_key={API_KEY}")  # Send a request to the endpoint
    # Convert the response to json and extract the data key
    line_data = response.json()["data"]
    # Extract the relevant data
    line = {
        "id": line_data["id"],
        "text_color": line_data["attributes"]["text_color"],
        "short_name": line_data["attributes"]["short_name"],
        "long_name": line_data["attributes"]["long_name"],
        "color": line_data["attributes"]["color"],
    }
    # Return the data to the user
    return {"lines": line}