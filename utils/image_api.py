import os
import requests

API_KEY = os.getenv("PEXELS_API_KEY")

HEADERS = {
    "Authorization": API_KEY
}

def get_place_image(place_name):
    url = "https://api.pexels.com/v1/search"

    params = {
        "query": place_name,
        "per_page": 1
    }

    response = requests.get(url, headers=HEADERS, params=params)

    if response.status_code == 200:
        data = response.json()

        if len(data["photos"]) > 0:
            return data["photos"][0]["src"]["large"]

    return None