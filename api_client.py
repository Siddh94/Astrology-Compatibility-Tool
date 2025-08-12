
from config import GOOGLE_API_KEY

def get_coordinates(place_name):
    """Fetch latitude & longitude using Google Geocoding API."""
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={place_name}&key={GOOGLE_API_KEY}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    if data["status"] != "OK":
        raise ValueError(f"Geocoding failed: {data['status']}")

    location = data["results"][0]["geometry"]["location"]
    return location["lat"], location["lng"]

