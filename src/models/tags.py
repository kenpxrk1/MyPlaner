from .base import Base, str_25
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str_25]
    color: Mapped[str]
    owner_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete="CASCADE")) 

