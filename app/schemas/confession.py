from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


# schema with a common fields
class ConfessionBase(BaseModel):
    confession: str

# creating confession
class ConfessionCreate(ConfessionBase):
    pass

# receiving confession
class Confession(ConfessionBase):
    id: str
    confession: str
    created_at: datetime
    comments: Optional[List["Comment"]] = None

    class Config:
        orm_mode = True

# Import Comment here to avoid circular imports
from app.schemas.comment import Comment
Confession.model_rebuild()
