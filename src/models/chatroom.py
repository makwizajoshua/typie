from message import Message
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base
from models.user import User


class ChatRoom(Base):
    __tablename__ = "chatrooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    client_ids: Mapped[list[int]] = mapped_column(ForeignKey("users.id"), index=True)

    clients: Mapped["User"] = relationship(back_populate="users", cascade="all, delete-orphan")
    messages: Mapped[list["Message"]] = relationship(back_populates="catroom")
