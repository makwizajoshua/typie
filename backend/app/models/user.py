from datetime import UTC, datetime

from backend.app.models.chatroom import ChatRoom
from backend.app.schemas.auth_credentials import AuthenticatedUser
from db import Base
from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )
    chatroom_ids: Mapped[list[int]] = mapped_column(ForeignKey("chatrooms.id"))

    chatrooms: Mapped[list["ChatRoom"]] = relationship(
        back_populates="chatrooms", cascade="all, delete-orphan"
    )

    def toAuthUser(self) -> AuthenticatedUser:
        return AuthenticatedUser(
            id=self.id,
            username=self.username,
        )
