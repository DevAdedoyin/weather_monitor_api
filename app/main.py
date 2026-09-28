from datetime import datetime
import os
import json
from urllib import response
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
from openai import OpenAI
from IPython.display import Markdown, display

from app.chat_response import SearchLocationWeatherChat



deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')

app = FastAPI()

@app.get("/api/prompt")
async def get_user_prompt(user_prompt: str, lat: float, lon: float, current_location: str, date: str = datetime.now().strftime("%d-%m-%Y %H:%M:%S")):
    response = await SearchLocationWeatherChat.search_location_weather_chat(
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
