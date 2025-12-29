from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# schema with a common fields
class ConfessionBase(BaseModel):
    confession: str

# creating confession
class ConfessionCreate(ConfessionBase):
    pass

# recieving confession
class Confession(ConfessionBase):
    id: str
    confession: str
    created_at: datetime

    class Config:
        orm_mode = True

