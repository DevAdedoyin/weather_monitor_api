
from datetime import datetime, timezone

from pydantic import BaseModel, ConfigDict, Field


class UserChatCreate(BaseModel):
    is_authenticated: bool = False


class ChatMessageCreate(BaseModel):
    content: str = Field(min_length=1)


class ChatMessageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    role: str
    content: str
    created_at: datetime


class UserChatResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_chat_id: str
    created_at: datetime
    last_used: datetime
    is_authenticated: bool
    messages: list[ChatMessageResponse] = Field(default_factory=list)
