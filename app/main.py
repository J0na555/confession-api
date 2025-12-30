from fastapi import FastAPI
from app.api.v1.endpoints import routes, comments, votes
from app.db.database import engine
from fastapi.middleware.cors import CORSMiddleware
from app.db.base import Base
from app.models import Confession, Comment, Vote

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Anonymous Confession API")

app.include_router(
    routes.router,
    prefix="/api/v1/confessions",
    tags=["confessions"]
)

app.include_router(
    comments.router,
    prefix="/api/v1/comments",
    tags=["comments"]
)

app.include_router(
    votes.router,
    prefix="/api/v1",
    tags=["votes"]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=False, 
    allow_methods=["*"], 
    allow_headers=["*"],  
)
@app.get("/")
def root():
    return{"message":"Anonymous confession api"}

