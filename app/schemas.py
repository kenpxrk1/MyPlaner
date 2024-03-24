from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel, EmailStr

""" USER SCHEMA """
class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config():
        from_attributes = True

""" AUTH SCHEMA """

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None

""" TASK SCHEMA """

class TaskBase(BaseModel):
    title: str
    content: str
    starts_at: date


class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    created_at: datetime
    owner_id: int
    tags: Optional[list] = None
    owner: UserOut

    class Config:
        from_attributes = True

class TaskUpdate(TaskBase):
    pass 

""" TAG SCHEMA """

class Tag(BaseModel):
    id: int
    description: str

