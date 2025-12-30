from sqlalchemy import Column, String, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.db.base import Base

class Comment(Base):
    __tablename__ = 'comment'

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True 
    )
    confession_id = Column(
        String,
        ForeignKey('confession.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    comment = Column(
        Text,
        nullable=False
    )
    created_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(),
        nullable=False
    )
    
    # Relationship with confession
    confession = relationship("Confession", back_populates="comments")
