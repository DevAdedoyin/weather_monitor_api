
import json
from urllib.error import URLError
from urllib.request import urlopen

from helpers.url_loader import URLLoader


class WeatherData:

    @staticmethod
    def get_weather_data(lat: float, lon: float, isHistory: bool, location: str, timestamp: int | None = None):
        """This function retrieves weather data for a given location and timestamp."""

        try:
            url = URLLoader.load_openweather_url(lat, lon, isHistory=isHistory, timestamp=timestamp)

            print(f"Calling URL: {url}")

            with urlopen(url, timeout=10) as response:
                results = json.loads(response.read().decode("utf-8"))
        except (URLError, TimeoutError, ValueError, json.JSONDecodeError) as exc:
            raise RuntimeError(f"Failed to fetch weather data for '{location}': {exc}") from exc

        if not results:
            raise LookupError(f"No weather data found for location: {location}")

        return results

