import datetime
from typing import List, Optional
from pydantic import BaseModel

from .tag import TagBase 

class TaskCreate(BaseModel):
    title: str 
    content: str 
    starts_at: datetime.date 


class TaskRead(TaskCreate):

    tags: list | None


class TaskBase(TaskCreate):
    id: int
    owner_id: int 
    tags: List[TagBase] | None = None
    

class TaskUpdate(TaskCreate):
    pass 
