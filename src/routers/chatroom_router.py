from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.db import get_db
from src.models.chatroom_model import ChatRoom
from src.models.user_model import User
from src.schemas.chatroom_schema import ChatroomBase

router = APIRouter(prefix="/chatroom")


@router.get("/all/{user_id}")
def get_all_chatrooms(user_id: int, db: Annotated[Session, Depends(get_db)]):
    statement = select(ChatRoom).join(ChatRoom.clients).where(User.id == user_id)
    return db.execute(statement).all()


@router.post("/create")
def create_chatroom(
    chatroom_data: ChatroomBase,
    db: Annotated[Session, Depends(get_db)],
):

    clients = db.execute(select(User).where(User.id.in_(chatroom_data.clients))).scalars().all()
    if not clients:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail={"error": "No valid clients found"}
        )

    chatroom_clients = list(set(clients))
    new_chatroom = ChatRoom(name=chatroom_data.name, clients=chatroom_clients)

    db.add(new_chatroom)
    db.commit()
    db.refresh(new_chatroom)

    return {"message": "Chatroom created successfully", "chatroom_id": new_chatroom.id}


@router.post("/join/{chatroom_id}")
def join_chatroom(chatroom_id: int, user_id: int, db: Annotated[Session, Depends(get_db)]):
    chatroom = db.get(ChatRoom, chatroom_id)
    user = db.get(User, user_id)

    if not chatroom:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail={"error": "Chatroom not found"}
        )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail={"error": "User not found"}
        )

    if user not in chatroom.clients:
        chatroom.clients.append(user)
        db.commit()
        db.refresh(chatroom)

    return {"message": "User joined chatroom successfully", "chatroom": chatroom}


@router.patch("/update/{chatroom_id}", status_code=status.HTTP_200_OK)
def edit_chatroom(
    chatroom_id: int, chatroom_data: ChatroomBase, db: Annotated[Session, Depends(get_db)]
):
    chatroom = db.get(ChatRoom, chatroom_id)
    if not chatroom:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail={"error": "Chatroom not found"}
        )

    new_clients = db.execute(select(User).where(User.id.in_(chatroom_data.clients))).scalars().all()
    if not new_clients:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail={"error": "No valid clients found"}
        )

    new_clients = []
    new_clients.extend(chatroom.clients)
    new_clients.extend(
        db.execute(select(User).where(User.id.in_(chatroom_data.clients))).scalars().all()
    )
    chatroom.clients = list(set(new_clients))

    db.commit()
    db.refresh(chatroom)

    return {"message": "Chatroom updated successfully", "chatroom": chatroom}


@router.delete("/delete/{chatroom_id}")
def delete_chatroom(chatroom_id: int, db: Annotated[Session, Depends(get_db)]):
    chatroom = db.get(ChatRoom, chatroom_id)
    if not chatroom:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail={"error": "Chatroom not found"}
        )

    db.delete(chatroom)
    db.commit()

    return {"message": "Chatroom deleted successfully"}
