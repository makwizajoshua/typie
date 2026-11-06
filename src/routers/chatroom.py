from fastapi import APIRouter

router = APIRouter(prefix="/chatroom")


@router.websocket("/{chatroom_id}")
def enter_roo():
    return "enter iner"
