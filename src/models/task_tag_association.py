from typing import List
from .base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column


class Task_tag_association(Base):

    __tablename__ = "task_tag_association"

    tag_id: Mapped[int] = mapped_column(
        ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True
    )
    task_id: Mapped[int] = mapped_column(
        ForeignKey("tasks.id", ondelete="CASCADE"), primary_key=True
    )
    tasks: Mapped[List["Task"] | None] = relationship(  # type: ignore
        back_populates="tags"
    )
