from fastapi import FastAPI
from app.api.v1.endpoints import routes
from app.db.database import engine
from app.db.base import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Anonymous Confession API")

app.include_router(
    routes.router,
    prefix="/api/v1/confessions",
    tags=["confessions"]
)

@app.get("/")
def root():
    return{"message":"Anonymous confession api"}

