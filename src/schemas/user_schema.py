from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    username: str = Field(max_length=256)
    email: EmailStr = Field(max_length=128)


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    pass


class UserLogin(UserBase):
    pass
