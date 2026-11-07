from pydantic import BaseModel, Field


class ChatroomBase(BaseModel):
    name: str = Field(max_length=100)
    clients: list[int] = Field(default_factory=list)


ChatroomCreate = ChatroomBase
ChatroomUpdate = ChatroomBase
