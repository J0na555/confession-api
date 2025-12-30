from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


# Schema with common fields
class CommentBase(BaseModel):
    comment: str

# Creating comment
class CommentCreate(CommentBase):
    confession_id: str

# Receiving comment
class Comment(CommentBase):
    id: str
    confession_id: str
    comment: str
    created_at: datetime
    upvotes: int = 0
    downvotes: int = 0
    score: int = 0  # upvotes - downvotes

    class Config:
        orm_mode = True
