from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base
from models.chatroom import ChatRoom
from schemas.auth_credentials import AuthenticatedUser


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )
    image_file: Mapped[str | None] = mapped_column(String(200), nullable=True, default=None)
    chatroom_ids: Mapped[list[int]] = mapped_column(ForeignKey("chatrooms.id"))

    chatrooms: Mapped[list["ChatRoom"]] = relationship(
        back_populates="chatrooms", cascade="all, delete-orphan"
    )

    @property
    def image_path(self):
        if self.image_file:
            return f"/media/pfp/{self.image_file}"
        else:
            return "static/media/pfp.png"

    def toAuthUser(self) -> AuthenticatedUser:
        return AuthenticatedUser(
            id=self.id,
            username=self.username,
        )
