from fastapi import APIRouter, Depends
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from db import get_db
from models.message import Message
from models.user import User
from schemas.message_body import MessageBody
from util import get_current_user

router = APIRouter(prefix="/message", tags=["message"])


@router.get("/all/{chatroom_id}")
def get_all_messages(chatroom_id: int, db: Session = Depends(get_db)):
    statement = select(Message).where(Message.chatroom_id == chatroom_id)
    messages = db.scalars(statement)
    return messages


@router.post("/message")
def send_message(
    message_body: MessageBody,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    message = Message(author=user.id, content=message_body.content)

    db.add(message)
    db.commit()
    db.refresh(message)
    return {"message": "message sent successfully"}
