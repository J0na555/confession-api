from fastapi import FastAPI
from app.api.v1.endpoints import routes
from app.db.database import engine
from fastapi.middleware.cors import CORSMiddleware
from app.db.base import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Anonymous Confession API")

app.include_router(
    routes.router,
    prefix="/api/v1/confessions",
    tags=["confessions"]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173', 'https://student-confession-page1-soxi.vercel.app/'],
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)
@app.get("/")
def root():
    return{"message":"Anonymous confession api"}

