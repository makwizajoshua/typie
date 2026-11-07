from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base
from models.chatroom_model import ChatRoom


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    author: Mapped[int] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(String(512), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC))
    chatroom_id: Mapped[int] = mapped_column(ForeignKey("chatrooms.id"), index=True)

    chatroom: Mapped["ChatRoom"] = relationship(back_populates="messages")
