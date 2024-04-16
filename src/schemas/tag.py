from pydantic import BaseModel


class TagBase(BaseModel):
    title: str
    color: str 

