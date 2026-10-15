
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserChatBase(BaseModel):
    user_chat_id: str = Field(min_length=1, max_length=70)
    created_at: datetime = Field(default_factory=datetime.now)
    isAuthenticated: bool = Field(default=False)
    chat_history: list[dict] = Field(default_factory=list)



class UserChatCreate(UserChatBase):
    pass


class UserChatResponse(UserChatBase):
    model_config = ConfigDict(from_attributes=True)

    last_used: datetime = Field(default_factory=datetime.now)
