from fastapi import FastAPI, Depends
import requests
from configuration.config import ServerSettings
from security.auth import authenticate
from configuration.config import Message
from fastapi.responses import JSONResponse
from starlette import status

route_app = FastAPI()


def build_server_config():
    return ServerSettings()

# Get a list of all routes
@route_app.get("/")
def get_routes(sconfig:ServerSettings = Depends(build_server_config), user: dict = Depends(authenticate)):
    routes_list = list()
    response = requests.get(sconfig.endpoint+f"/routes?&api_key={sconfig.api_key}") # Send a request to the endpoint

    if response.status_code == 400:
        return JSONResponse(status_code=400, content={"message": f"Bad Request"}) # Return Error for a 400 response code
    elif response.status_code == 403:
        return JSONResponse(status_code=403, content={"message": f"API Request Forbidden"}) # Return Error for a 403 response code
    elif response.status_code == 429:
        return JSONResponse(status_code=429, content={"message": f"Too Many Requests"}) # Return Error for a 429 response code

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
@route_app.get("/{route_id}")
def get_route(route_id: str,
              sconfig:ServerSettings = Depends(build_server_config),
              user: dict = Depends(authenticate)):
    response = requests.get(sconfig.endpoint + f"/routes/{route_id}?api_key={sconfig.api_key}") # Send a request to the endpoint

    if response.status_code == 400:
        return JSONResponse(status_code=400, content={"message": f"Bad Request"}) # Return Error for a 400 response code
    elif response.status_code == 403:
        return JSONResponse(status_code=403, content={"message": f"API Request Forbidden"}) # Return Error for a 403 response code
    elif response.status_code == 404:
        return JSONResponse(status_code=404, content={"message": f"Route {route_id} not found"})
    elif response.status_code == 406:
        return JSONResponse(status_code=406, content={"message": f"Not Acceptable"})
    elif response.status_code == 429:
        return JSONResponse(status_code=429, content={"message": f"Too Many Requests"}) # Return Error for a 429 response code

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
    return {"route": route}