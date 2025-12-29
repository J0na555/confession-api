from sqlalchemy import Column, String, DateTime
from datetime import datetime
import uuid

from app.db.base import Base

class Confession(Base):
    __table__='confession'

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True 
    ) 
    confession = Column(
        String,
        nullable=False
   )
    created_at = Column(
        DateTime,
        default=datetime.utc.now,
        nullable=False
   )


   
   