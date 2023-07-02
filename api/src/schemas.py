from typing import List, Optional
from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: List[Item] = []

    class Config:
        orm_mode = True


class SessionBase(BaseModel):
    user_id: str


class SessionCreate(SessionBase):
    password: str


class SessionValidate(SessionBase):
    random_string: str


class Session(SessionBase):
    id: int
    is_active: bool
    random_string: str

    class Config:
        orm_mode = True
