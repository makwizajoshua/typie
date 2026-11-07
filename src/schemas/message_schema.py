from datetime import UTC, datetime

from pydantic import BaseModel, Field


class MessageBase(BaseModel):
    content: str = Field(max_length=512)
    created_at: datetime = Field(default=datetime.now(UTC))
    author_id: int
    chatroom_id: int


MessageCreate = MessageBase
MessageResponse = MessageBase
