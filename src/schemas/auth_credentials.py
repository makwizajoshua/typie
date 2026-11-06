from pydantic import BaseModel, Field


class Credentials(BaseModel):
    username: str = Field(min_length=3, max_length=256)
    password: str = Field(min_length=6, max_length=50)


class AuthenticatedUser(BaseModel):
    id: int
    username: str

    model_config = {"from_attributes": True}
