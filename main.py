import requests
import json
from fastapi import APIRouter, FastAPI
from pydantic import BaseModel
import uvicorn
from fastapi.middleware.cors import CORSMiddleware


class WeatherRequest(BaseModel):
    street: str
    city: str
    state: str | None = None
    zip_code: int
    style: str | None = "f"


app = FastAPI(redirect_slashes=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/weather/")
async def weather(req_data: WeatherRequest):
    state_zip = ""
    if req_data.zip_code > 0:
        state_zip = f"&zip={req_data.zip_code}"
    if req_data.state is not None:
        state_zip = f"&state={req_data.state}" + state_zip

    # Run forward geocoding on the address
    res = requests.get(
        f'https://geocoding.geo.census.gov/geocoder/locations/address?street={req_data.street}&city={req_data.city}{state_zip}&benchmark=Public_AR_Census2020&format=json')
    coords = res.json().get("result", {}).get(
        "addressMatches", [])

    if not len(coords):
        print(coords)
        return {"msg": "Could not obtain coordinates"}

    coords = coords[0].get("coordinates", {})

    if coords:
        # If we got the coordinates, get forecast office ID and forecast grid coordinates
        res = requests.get(
            f'https://api.weather.gov/points/{coords["y"]}%2C{coords["x"]}')
    else:
        return {"msg": "Could not obtain coordinates"}

    geo_json = res.json().get("properties", {})

    if not geo_json:
        return {"msg": "Could not obtain forecast office ID and forecast grid coordinates"}

    # # Uncomment for forecast
    # # If we got forecast office ID and forecast grid coordinates, get forecast
    # res = requests.get(
    #     f'https://api.weather.gov/gridpoints/{geo_json["gridId"]}/{geo_json["gridX"]}%2C{geo_json["gridY"]}')

    # Get station ID
    res = requests.get(
        f'https://api.weather.gov/gridpoints/{geo_json["gridId"]}/{geo_json["gridX"]}%2C{geo_json["gridY"]}/stations')

    stations = res.json().get("observationStations", [])

    if not len(stations):
        return {"msg": "Could not obtain observation stations IDs"}

    station_id = stations[0][stations[0].rindex("/") + 1:]

    if not len(station_id):
        return {"msg": "Could not obtain observation station ID"}

    # Get the latest observation
    res = requests.get(
        f'https://api.weather.gov/stations/{station_id}/observations/latest')

    props = res.json().get("properties", {})

    if not props:
        return {"msg": "Could not obtain the latest observation"}

    reply = dict()

    reply["temperature"] = props["temperature"]["value"]
    reply["windSpeed"] = props["windSpeed"]["value"]
    reply["relativeHumidity"] = props["relativeHumidity"]["value"]

    if reply["temperature"] is not None and req_data.style == "f":
        reply["temperature"] = reply["temperature"] * 9 / 5 + 32

    return reply

# print(json.dumps(res.json(), indent=2))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
