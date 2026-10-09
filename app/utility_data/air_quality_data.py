
import httpx
from helpers.url_loader import URLLoader
from datetime import datetime, timezone


class AirQualityData:

    @staticmethod
    async def get_air_quality_data(location: str, lat: float, lon: float):
        """This function retrieves current air quality data for a given location.
        It constructs a payload with the location coordinates and sends a POST request to the Google Air Quality API."""

        data = {
                "location": {
                    "latitude": lat,
                    "longitude": lon,
                    },
                "extraComputations": [
                    "HEALTH_RECOMMENDATIONS",
                    "DOMINANT_POLLUTANT_CONCENTRATION",
                    "POLLUTANT_CONCENTRATION",
                    "LOCAL_AQI",
                    "POLLUTANT_ADDITIONAL_INFO"
                    ],
                "uaqiColorPalette": "COLOR_PALETTE_UNSPECIFIED",
                "customLocalAqis": [],
                "universalAqi": True,
                "languageCode": "en"
            }

        url = URLLoader.load_airquality_url()

        try:
            response = httpx.post(
                url,
                json=data,
                timeout=10,
                headers={ "Content-Type": "application/json" }
            )

            if response.status_code == 400:
                data = response.json()

                if data.get("error", {}).get("status") == "INVALID_ARGUMENT":
                    return {
                        "available": False,
                        "message": data.get("error", {}).get("message")
                    }

            response.raise_for_status()
            results = response.json()
            return results
        except httpx.HTTPError as exc:
            raise RuntimeError(f"Failed to fetch current air quality data for '{location}': {exc}") from exc


    @staticmethod
    async def get_historical_air_quality_data(location: str, lat: float, lon: float,):
        """This function retrieves historical air quality data for a given location and timestamp.
        It constructs a payload with the location coordinates and the specified timestamp."""

        payload = {
                    "hours": 720,
                    "location": {
                        "latitude": lat,
                        "longitude": lon
                    }
                }

        url = URLLoader.load_airquality_url(urlType="historical")

        try:
            response = httpx.post(
                        url,
                        json=payload,
                        timeout=10,
                        headers={ "Content-Type": "application/json" }
                    )

            if response.status_code == 400:
                data = response.json()

                if data.get("error", {}).get("status") == "INVALID_ARGUMENT":
                    return {
                        "available": False,
                        "message": data.get("error", {}).get("message")
                    }

            response.raise_for_status()
            results = response.json()
            return results
        except httpx.HTTPError as exc:
            raise RuntimeError(f"Failed to fetch historical air quality data for '{location}': {exc}") from exc


    @staticmethod
    async def get_forecast_air_quality_data(location: str, lat: float, lon: float, timestamp: str):
        """This function retrieves forecast air quality data for a given location and timestamp.
        It constructs a payload with the location coordinates and the specified timestamp."""

        payload = {
                    "pageSize": "10",
                    "universalAqi": "true",
                    "location": {
                        "latitude": lat,
                        "longitude": lon,
                    },
                    "dateTime": timestamp,
                    "languageCode": "en",
                    "extraComputations": [
                        "HEALTH_RECOMMENDATIONS",
                        "DOMINANT_POLLUTANT_CONCENTRATION",
                        "POLLUTANT_ADDITIONAL_INFO",
                    ],
                    "uaqiColorPalette": "RED_GREEN"
                }

        url = URLLoader.load_airquality_url(urlType="forecast")

        try:
            response = httpx.post(
                        url,
                        json=payload,
                        timeout=10,
                        headers={ "Content-Type": "application/json" }
                    )

            if response.status_code == 400:
                data = response.json()

                if data.get("error", {}).get("status") == "INVALID_ARGUMENT":
                    return {
                        "available": False,
                        "message": data.get("error", {}).get("message")
                    }

            response.raise_for_status()
            results = response.json()
            return results
        except httpx.HTTPError as exc:
            raise RuntimeError(f"Failed to fetch forecast air quality data for '{location}': {exc}") from exc

