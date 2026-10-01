import os

class APIKeyLoader:

    # API key for OpenWeather weather data
    def load_openweather_api_key():
        api_key = os.getenv("OPEN_WEATHER_API_KEY")
        if not api_key:
            raise RuntimeError("OPENWEATHER_API_KEY is not configured")
        return api_key

    # API key for the air quality data
    def load_google_cloud_api_key():
        api_key = os.getenv("GOOGLE_CLOUD_KEY")
        if not api_key:
            raise RuntimeError("GOOGLE_CLOUD_KEY is not configured")
        return api_key

