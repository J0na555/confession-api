from sqlalchemy import Column, String, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.db.base import Base

class Vote(Base):
    __tablename__ = 'vote'

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        index=True
    )
    comment_id = Column(
        String,
        ForeignKey('comment.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    # Using IP address to track votes (for anonymous system)
    voter_ip = Column(
        String,
        nullable=False,
        index=True
    )
    # 1 for upvote, -1 for downvote
    vote_value = Column(
        Integer,
        nullable=False
    )
    
    # Ensure one vote per IP per comment
    __table_args__ = (
        UniqueConstraint('comment_id', 'voter_ip', name='unique_vote_per_ip'),
    )
    
    # Relationship with comment
    comment = relationship("Comment", back_populates="votes")
