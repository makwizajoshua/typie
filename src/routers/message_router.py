from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from core.connection_manager import ConnectionManager
from db import get_db
from src.models.message_model import Message
from src.schemas.message_schema import MessageResponse

router = APIRouter(prefix="/message", tags=["message"])
manager = ConnectionManager()


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


@router.websocket("/message/{client_id}/{chatroom_id}")
async def chatroom_ws_endpoint(
    websocket: WebSocket,
    client_id: int,
    chatroom_id: int,
    db: Session = Depends(get_db),
):
    await manager.connect(websocket)

    try:
        while True:
            data = await websocket.receive_text()

            db_message = Message(content=data, author_id=client_id, chatroom_id=chatroom_id)
            db.add(db_message)
            db.commit()

            db.refresh(db_message)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast_message(f"{client_id} has disconnected")
