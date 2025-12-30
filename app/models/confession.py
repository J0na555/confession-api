from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.db.base import Base

class Confession(Base):
    __tablename__ = 'confession'

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True 
    ) 
    confession = Column(
        Text,
        nullable=False
   )
    created_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(),
        nullable=False
   )
    
    # Relationship with comments
    comments = relationship("Comment", back_populates="confession", cascade="all, delete-orphan")



   