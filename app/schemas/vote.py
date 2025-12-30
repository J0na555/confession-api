from pydantic import BaseModel
from typing import Optional


class VoteCreate(BaseModel):
    comment_id: str
    voter_ip: str
    vote_value: int  # 1 for upvote, -1 for downvote


class VoteResponse(BaseModel):
    id: str
    comment_id: str
    vote_value: int
    
    class Config:
        orm_mode = True
