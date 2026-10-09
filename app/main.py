from datetime import datetime
from fastapi import FastAPI

from chat_response import WeatherChat


app = FastAPI()

"""This endpoint receives the user's question and the resolved location metadata.
The chat layer then decides whether the request needs weather or air-quality data
before building the final text response back to the client."""
@app.get("/api/prompt")
async def get_user_prompt(user_prompt: str, lat: float, lon: float, current_location: str, date: str = datetime.now().strftime("%d-%m-%Y %H:%M:%S")):
    response = await WeatherChat.weather_chatter(
        user_prompt,
        lat=lat,
        lon=lon,
        location=current_location,
        date=date
    )

    return {
        "chat_response": response,
        "date": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
    }
