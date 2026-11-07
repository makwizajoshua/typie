from fastapi import APIRouter, Depends
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from core.connection_manager import ConnectionManager
from db import get_db
from src.models.message_model import Message
from src.schemas.message_schema import MessageCreate, MessageResponse

router = APIRouter(prefix="/message", tags=["message"])
connection_manager = ConnectionManager()


@router.get("/all/{chatroom_id}", response_model=list[MessageResponse])
def get_all_messages(chatroom_id: int, db: Session = Depends(get_db)):
    statement = select(Message).where(Message.chatroom_id == chatroom_id)
    messages = db.scalars(statement)
    _msg = []
    for message in messages:
        _msg.append(
            MessageResponse(
                content=message.content,
                created_at=message.created_at,
                author_id=message.author,
                chatroom_id=message.chatroom_id,
            )
        )
    return messages


@router.websocket("/message/ws/{chatroom_id}")
def send_message(
    message: MessageCreate,
    db: Session = Depends(get_db),
):
    created_message = Message(
        author=message.author_id, content=message.content, chatroom_id=message.chatroom_id
    )

    db.add(created_message)
    db.commit()
    db.refresh(created_message)
    return {"message": "message sent successfully"}
