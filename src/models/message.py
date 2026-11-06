from datetime import UTC, datetime

from chatroom import ChatRoom
from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    author: Mapped[int] = mapped_column(nullable=False)
    recipient: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC))
    chatroom_id: Mapped[int] = mapped_column(ForeignKey("chatrooms.id"), index=True)

    chatroom: Mapped["ChatRoom"] = relationship(back_populates="chatroom")
