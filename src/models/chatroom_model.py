from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base
from models.message_model import Message
from models.user_model import User

chatroom_clients = Table(
    "chatroom_clients",
    Base.metadata,
    Column("chatroom_id", ForeignKey("chatrooms.id"), primary_key=True),
    Column("user_id", ForeignKey("users.id"), primary_key=True),
)


class ChatRoom(Base):
    __tablename__ = "chatrooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, index=True)

    clients: Mapped[list["User"]] = relationship(
        secondary=chatroom_clients, back_populates="chatrooms"
    )
    messages: Mapped[list["Message"]] = relationship(
        back_populates="chatroom", cascade="all, delete-orphan"
    )
