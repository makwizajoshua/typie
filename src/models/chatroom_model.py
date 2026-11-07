from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base
from src.models.message_model import Message
from src.models.user_model import User


class ChatRoom(Base):
    __tablename__ = "chatrooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, index=True)
    client_ids: Mapped[list[int]] = mapped_column(ForeignKey("users.id"), index=True)

    clients: Mapped[list["User"]] = relationship(
        back_populate="users", cascade="all, delete-orphan"
    )
    messages: Mapped[list["Message"]] = relationship(
        back_populates="chatroom", cascade="all, delete-orphan"
    )
