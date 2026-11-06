from datetime import UTC, datetime

from pydantic import BaseModel, Field


class MessageBody(BaseModel):
    content: str = Field(max_length=256)
    created_at: datetime = Field(default=datetime.now(UTC))
