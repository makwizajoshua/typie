from db import Base
from sqlalchemy.orm import Mapped, mapped_column


class ChatRoom(Base):
    __tablename__ = "chatrooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    node1: Mapped[int] = mapped_column(nullable=False)
    node2: Mapped[int] = mapped_column(nullable=False)
