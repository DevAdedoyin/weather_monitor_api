


import json

from urllib.request import urlopen

import httpx

from helpers.url_loader import URLLoader


class AirQualityData:

    @staticmethod
    def get_air_quality_data(location: str, lat: float, lon: float):
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

        print(f"Calling URL: {url}")

        response = httpx.post(
            url,
            json=data,
            timeout=10
        )

        response.raise_for_status()

        results = response.json()

        if not results:
            raise LookupError(f"No air quality data found for location: {location}")
        return results