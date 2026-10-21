
from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
import httpx
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.chat_response import WeatherChat
import database
import models
from database import get_db
from schemas import ChatMessageCreate, ChatMessageResponse, UserChatCreate, UserChatResponse


router = APIRouter()


"""This endpoint creates a new user chat session in the database and returns the created session details."""
@router.post("", response_model=UserChatResponse, status_code=status.HTTP_201_CREATED)
def create_user_chat(user_chat: UserChatCreate, db: Annotated[Session, Depends(database.get_db)]):

    result = db.execute(
        select(models.UserChat).where(models.UserChat.user_chat_id == user_chat.user_chat_id),
    )

    existing_user_chat = result.scalars().first()

    # print(f"Existing user chat: {existing_user_chat}")
    if existing_user_chat:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User chat session already exists",
        )

    new_user_chat = models.UserChat(
        user_chat_id=user_chat.user_chat_id,
        created_at=user_chat.created_at,
        is_authenticated=user_chat.is_authenticated,
        messages=[
            models.ChatMessage(
            role=msg.role,
            content=msg.content,
        )
        for msg in user_chat.chat_history
    ],)

    db.add(new_user_chat)
    db.commit()
    db.refresh(new_user_chat)

    return new_user_chat


"""Add a message and generate the weather response"""
@router.post("/{user_chat_id}/messages")
async def send_chat_message(user_chat_id: str, message: ChatMessageCreate, lat: float, lon: float, current_location: str,
    db: Annotated[Session, Depends(database.get_db)],):

    # Retrieve the session and existing conversation history
    user_chat = db.execute(
        select(models.UserChat)
        .options(selectinload(models.UserChat.messages))
        .where(models.UserChat.user_chat_id == user_chat_id)
    ).scalars().first()

    if user_chat is None:
        raise HTTPException(
            status_code=404,
            detail="Chat session not found",
        )

    # Build the context from previous messages
    chat_history = [
        {
            "role": msg.role,
            "content": msg.content,
        }
        for msg in user_chat.messages
    ]

    # Save the new user message
    user_message = models.ChatMessage(
        user_chat_id=user_chat_id,
        role="user",
        content=message.content,
    )

    db.add(user_message)
    user_chat.last_used = datetime.now(UTC)
    db.commit()

    # Generate a response using the previous conversation
    try:
        response = await WeatherChat.weather_chatter(
            user_prompt=message.content,
            lat=lat,
            lon=lon,
            location=current_location,
            date=datetime.now(UTC).isoformat(),
            chat_history=chat_history,
        )

        response_text = response.output_text

        if not response_text:
            raise HTTPException(
                status_code=502,
                detail="The weather assistant returned an empty response",
            )

        # Persist the assistant response
        assistant_message = models.ChatMessage(
            user_chat_id=user_chat_id,
            role="assistant",
            content=response_text,
        )

        db.add(assistant_message)
        user_chat.last_used = datetime.now(UTC)
        db.commit()
        db.refresh(assistant_message)

        return {
            "user_chat_id": user_chat_id,
            "chat_response": response_text,
            "message": ChatMessageResponse.model_validate(
                assistant_message
            ),
        }

    except HTTPException:
        raise
    except Exception:
        db.rollback()
        raise


"""Retrieve a session and its complete message history"""
@router.get("/{user_chat_id}", response_model=UserChatResponse,)
def get_user_chat(user_chat_id: str, db: Annotated[Session, Depends(database.get_db)],):

    user_chat = db.execute(
        select(models.UserChat)
        .options(selectinload(models.UserChat.messages))
        .where(models.UserChat.user_chat_id == user_chat_id)
    ).scalars().first()

    if user_chat is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat session not found",
        )

    return user_chat
