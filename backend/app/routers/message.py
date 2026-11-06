from backend.app.db import get_db
from backend.app.models.message import Message
from backend.app.models.user import User
from backend.app.schemas.message_body import MessageBody
from backend.app.util import get_current_user
from fastapi import APIRouter, Depends
from sqlalchemy.future import select
from sqlalchemy.orm import Session

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
