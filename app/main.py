from datetime import datetime

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from chat_response import WeatherChat


app = FastAPI()


@app.exception_handler(RuntimeError)
async def runtime_error_handler(_, exc: RuntimeError):
    return JSONResponse(status_code=503, content={"detail": str(exc)})


@app.exception_handler(ValueError)
async def value_error_handler(_, exc: ValueError):
    return JSONResponse(status_code=400, content={"detail": str(exc)})


@app.exception_handler(LookupError)
async def lookup_error_handler(_, exc: LookupError):
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(httpx.HTTPError)
async def http_error_handler(_, exc: httpx.HTTPError):
    return JSONResponse(status_code=503, content={"detail": f"External API request failed: {exc}"})


@app.exception_handler(Exception)
async def generic_exception_handler(_, exc: Exception):
    return JSONResponse(status_code=500, content={"detail": f"An unexpected error occurred: {exc}"})


"""This endpoint receives the user's question and the resolved location metadata.
The chat layer then decides whether the request needs weather or air-quality data
before building the final text response back to the client."""
@app.get("/api/prompt")
async def get_user_prompt(user_prompt: str, lat: float, lon: float, current_location: str, date: str = datetime.now().strftime("%d-%m-%Y %H:%M:%S")):
    try:
        response = await WeatherChat.weather_chatter(
            user_prompt,
            lat=lat,
            lon=lon,
            location=current_location,
            date=date
        )
    except (RuntimeError, ValueError, LookupError, httpx.HTTPError) as exc:
        raise HTTPException(status_code=503 if isinstance(exc, (RuntimeError, httpx.HTTPError)) else 400 if isinstance(exc, ValueError) else 404, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to process weather request: {exc}") from exc

    return {
        "chat_response": response.output_text,
        "response_id": response.id,
        "response_status": response.status,
        "model": response.model,
        "created_at": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
    }
