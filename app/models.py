
from pydantic import BaseModel
from sqlalchemy import *


from app.database import Base

class User(Base):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, 
                        server_default=text('now()'))


