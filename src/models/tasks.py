import datetime
from typing import List
from sqlalchemy import ForeignKey
from .base import Base, str_25
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str_25]
    content: Mapped[str]
    tags: Mapped[List["Tag"] | None] = relationship(         # type: ignore
        back_populates="tags"
    ) 
    starts_at: Mapped[datetime.date] 
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

