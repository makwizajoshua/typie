from datetime import UTC, datetime

from pydantic import BaseModel, Field


class MessageBase(BaseModel):
    content: str = Field(max_length=512)
    created_at: datetime = Field(default=datetime.now(UTC))
    author_id: int
    chatroom_id: int


MessageCreate = MessageBase


class MessageUpdate(BaseModel):
    content: str | None = Field(default=None, max_length=512)
    created_at: datetime | None = Field(default=None)
    author_id: int | None = Field(default=None)
    chatroom_id: int | None = Field(default=None)


MessageResponse = MessageBase
