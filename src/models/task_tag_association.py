
from .base import Base
from sqlalchemy import Column, ForeignKey, Table


association_table = Table(
    "association_table",
    Base.metadata,
    Column("tag_id", ForeignKey("tags.id"), primary_key=True, nullable=False),
    Column("task_id", ForeignKey("tasks.id"), primary_key=True, nullable=False),
)

