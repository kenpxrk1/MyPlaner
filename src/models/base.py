from typing import Annotated
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase


str_80 = Annotated[str, 80]
str_25 = Annotated[str, 25]

class Base(DeclarativeBase):
    type_annotation_map = {
         str_80: String(80),
         str_25: String(80)
    }