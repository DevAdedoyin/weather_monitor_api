from datetime import datetime

class URLLoader:
    @staticmethod
    def load_url(lat: float, lon: float, api_key: str, isHistory: bool, timestamp: int) -> str:
        count = 10
        if isHistory:
            return f"https://api.openweathermap.org/data/4.0/onecall/timeline/1day?cnt={count}&lat={lat}&lon={lon}&start={timestamp}&appid={api_key}"
        else:
            return f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={api_key}"
