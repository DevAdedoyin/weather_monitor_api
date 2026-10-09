
import json
from urllib.request import urlopen

from helpers.url_loader import URLLoader


class WeatherData:

    @staticmethod
    def get_weather_data(lat: float, lon: float, isHistory: bool, location: str, timestamp: int | None = None):
        """This function retrieves weather data for a given location and timestamp."""
        
        url = URLLoader.load_openweather_url(lat, lon, isHistory=isHistory, timestamp=timestamp)

        print(f"Calling URL: {url}")

        with urlopen(url, timeout=10) as response:
            results = json.loads(response.read().decode("utf-8"))

        if not results:
            raise LookupError(f"No weather data found for location: {location}")

        return results

