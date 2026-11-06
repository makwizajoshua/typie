from backend.app.models.user import User
from db import Base
from message import Message
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class ChatRoom(Base):
    __tablename__ = "chatrooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    client_ids: Mapped[list[int]] = mapped_column(ForeignKey("users.id"))

    clients: Mapped["User"] = relationship(back_populate="users", cascade="all, delete-orphan")
    messages: Mapped[list["Message"]] = relationship(back_populates="catroom")
