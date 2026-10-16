
from datetime import datetime, timezone

from pydantic import BaseModel, ConfigDict, Field

class ChatMessageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    role: str
    content: str
    created_at: datetime

class UserChatBase(BaseModel):
    user_chat_id: str = Field(min_length=1, max_length=70)
    created_at: datetime = Field(default_factory=datetime.now)
    is_authenticated: bool = Field(default=False)
    chat_history: list[ChatMessageResponse] = Field(default_factory=list)


class UserChatCreate(UserChatBase):
    pass


class ChatMessageCreate(BaseModel):
    content: str = Field(min_length=1)


class UserChatResponse(UserChatBase):
    model_config = ConfigDict(from_attributes=True)

    last_used: datetime
    chat_history: list[ChatMessageResponse] = Field(default_factory=list, validation_alias="messages",)


