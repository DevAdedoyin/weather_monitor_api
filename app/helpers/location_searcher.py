
import json
import os
from urllib.request import urlopen

from dotenv import load_dotenv
from geopy.geocoders import Nominatim

from helpers.url_loader import URLLoader


class LocationSearcher:
     # Function to search for weather information based on a location name
        def search_weather_for_location(location: str, isHistory: bool) -> dict[str, str | float | None]:
            """Resolve a place name to coordinates using OpenWeather geocoding."""

            load_dotenv()

            location = location.strip()
            if not location:
                raise ValueError("Location must not be empty")

            api_key = os.getenv("OPEN_WEATHER_API_KEY")
            if not api_key:
                raise RuntimeError("OPENWEATHER_API_KEY is not configured")

            # instantiate a new Nominatim client
            app = Nominatim(user_agent="weather_monitor_api", timeout=10)

            location_data = app.geocode(location)

            if location_data is None:
                raise LookupError(f"Could not find location: {location}")

            lat = location_data.latitude
            lon = location_data.longitude

            # Weather API to get weather information
            url = URLLoader.load_url(lat, lon, api_key, isHistory=isHistory)

            print(f"Calling URL: {url}")

            with urlopen(url, timeout=10) as response:
                results = json.loads(response.read().decode("utf-8"))

            if not results:
                raise LookupError(f"No weather data found for location: {location}")

            return results