import os
import json
from urllib import response
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
from openai import OpenAI
from IPython.display import Markdown, display

from tools.weather.location_search import LocationSearchWeatherTool



deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')

app = FastAPI()

@app.get("/api/prompt")
async def get_user_prompt(user_prompt: str):
    response = await LocationSearchWeatherTool.search_location_weather_chat(
        user_prompt
    )

    return {
        "prompt": response
    }
