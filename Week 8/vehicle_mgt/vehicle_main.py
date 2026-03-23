from fastapi import FastAPI, Depends
import httpx
from configuration.config import ServerSettings
from security.auth import authenticate
from fastapi.responses import JSONResponse

vehicle_app = FastAPI()#

def build_server_config():
    return ServerSettings()

# Dependency to fetch all alerts
async def get_all_vehicles(route: str = None, revenue: str = None, sconfig:ServerSettings = Depends(build_server_config)):
    params = {}
    if route:
        params["filter[route]"] = route
    if revenue:
        params["filter[revenue]"] = revenue

    async with httpx.AsyncClient() as client: # Define client
        response = await client.get(f"{sconfig.endpoint}/vehicles?api_key={sconfig.api_key}", params=params)
        return response

async def get_vehicle_by_id(vehicle_id:str, sconfig:ServerSettings = Depends(build_server_config)):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{sconfig.endpoint}/vehicles/{vehicle_id}?api_key={sconfig.api_key}")

        return response

@vehicle_app.get("/")
async def read_vehicles(response: httpx.Response=Depends(get_all_vehicles), user: dict = Depends(authenticate)):

    if response.status_code == 400:
        return JSONResponse(status_code=400, content={"message": f"Bad Request"}) # Return Error for a 400 response code
    elif response.status_code == 403:
        return JSONResponse(status_code=403, content={"message": f"API Request Forbidden"}) # Return Error for a 403 response code
    elif response.status_code == 429:
        return JSONResponse(status_code=429, content={"message": f"Too Many Requests"}) # Return Error for a 429 response code

    vehicles_list = []
    vehicles = response.json()["data"]

    for vehicle in vehicles:
        vehicles_list.append({
            "id": vehicle["id"],
            "updated_at": vehicle["attributes"]["updated_at"],
            "speed": vehicle["attributes"]["speed"],
            "revenue": vehicle["attributes"]["revenue"],
            "current_status": vehicle["attributes"]["current_status"],
        })

    return {"vehicles": vehicles_list}

@vehicle_app.get("/{vehicle_id}")
async def read_vehicle(vehicle_id:str,response: httpx.Response=Depends(get_vehicle_by_id), user: dict = Depends(authenticate)):

    if response.status_code == 400:
        return JSONResponse(status_code=400, content={"message": f"Bad Request"}) # Return Error for a 400 response code
    elif response.status_code == 403:
        return JSONResponse(status_code=403, content={"message": f"API Request Forbidden"}) # Return Error for a 403 response code
    elif response.status_code == 404:
        return JSONResponse(status_code=404, content={"message": f"Route {vehicle_id} not found"})
    elif response.status_code == 406:
        return JSONResponse(status_code=406, content={"message": f"Not Acceptable"})
    elif response.status_code == 429:
        return JSONResponse(status_code=429, content={"message": f"Too Many Requests"}) # Return Error for a 429 response code

    vehicle_data = response.json()["data"]

    vehicle = {
            "id": vehicle_data["id"],
            "updated_at": vehicle_data["attributes"]["updated_at"],
            "speed": vehicle_data["attributes"]["speed"],
            "revenue": vehicle_data["attributes"]["revenue"],
            "current_status": vehicle_data["attributes"]["current_status"],
        }

    return {"vehicle": vehicle}
