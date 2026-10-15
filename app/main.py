from datetime import datetime
from typing import Annotated
from fastapi.params import Depends
import httpx
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from database import get_db
import models
from sqlalchemy.orm import Session
from chat_response import WeatherChat
from schemas import UserChatCreate, UserChatResponse
from sqlalchemy import select


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

"""This endpoint creates a new user chat session in the database and returns the created session details."""
@app.post("/api/user_chats", response_model=UserChatResponse, status_code=status.HTTP_201_CREATED)
def create_user_chat(user_chat: UserChatCreate, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(
        select(models.UserChat).where(models.UserChat.user_chat_id == user_chat.user_chat_id),
    )

    existing_user_chat = result.scalars().first()

    if existing_user_chat:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User chat session already exists",
        )

    new_user_chat = models.UserChat(
        user_chat_id=user_chat.user_chat_id,
        created_at=user_chat.created_at,
        is_authenticated=user_chat.isAuthenticated,
        messages=[models.ChatMessage(role=msg.get("role"), content=msg.get("content")) for msg in user_chat.chat_history],
    )

    db.add(new_user_chat)
    db.commit()
    db.refresh(new_user_chat)

    return new_user_chat