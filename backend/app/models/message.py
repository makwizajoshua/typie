from datetime import UTC, datetime

from db import Base
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column


class Message(Base):
    __tablename__ = "messages"

    author: Mapped[int] = mapped_column(nullable=False)
    recipient: Mapped[int] = mapped_column(nullable=False)
    created_at: datetime = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )
