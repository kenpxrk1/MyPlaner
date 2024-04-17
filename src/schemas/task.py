import datetime
from typing import List, Optional
from pydantic import BaseModel

from .tag import TagBase 

class TaskCreate(BaseModel):
    title: str 
    content: str 
    starts_at: datetime.date 


class TaskRead(TaskCreate):

    tags: list["TagBase"] 

    class Config:
        from_attributes = True


class TaskBase(TaskCreate):
    id: int
    owner_id: int 
    tags: list["TagBase"] 
    

class TaskUpdate(TaskCreate):
    pass 
