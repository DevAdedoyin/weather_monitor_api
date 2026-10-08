


from urllib.request import urlopen
import httpx
from helpers.url_loader import URLLoader
from datetime import datetime, timezone


class AirQualityData:

    @staticmethod
    async def get_air_quality_data(location: str, lat: float, lon: float):
        # Air Quality API to get air quality information
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

        response = httpx.post(
            url,
            json=data,
            timeout=10,
            headers={ "Content-Type": "application/json" }
        )

        if response.status_code == 400:
            data = response.json()

            if data.get("error", {}).get("message") == (
                "Information is unavailable for this location. Please try a different location."
                ):
                return {
                    "available": False,
                    "message": f"Air quality information is unavailable for {location}."
                }

        response.raise_for_status()

        results = response.json()

        return results


    @staticmethod
    async def get_historical_air_quality_data(location: str, lat: float, lon: float,):

        payload = {
                    "hours": 720,
                    "location": {
                        "latitude": lat,
                        "longitude": lon
                    }
                }

        url = URLLoader.load_airquality_url(urlType="historical")

        response = httpx.post(
                    url,
                    json=payload,
                    timeout=10,
                    headers={ "Content-Type": "application/json" }
                )

        if response.status_code == 400:
            data = response.json()

            if data.get("error", {}).get("message") == (
                "Information is unavailable for this location. Please try a different location."
                ):
                return {
                    "available": False,
                    "message": f"Air quality information is unavailable for {location}."
                }

        response.raise_for_status()

        results = response.json()

        return results

