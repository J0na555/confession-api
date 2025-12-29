from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.database  import get_db
from app import schemas, services

router = APIRouter()

@router.post("/", response_model=schemas.Confession)
def create_confession(
    confession: schemas.ConfessionCreate,
    db: Session = Depends(get_db)
):
    return services.ConfessionService.create_confession(db, confession)


@router.get("/", response_model=List[schemas.Confession])
def read_confessions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    confessions = services.ConfessionService.get_confessions(db, skip, limit)
    return confessions

@router.get("/{confession_id}", response_model=schemas.Confession)
def read_confession(
    confession_id: str,
    db: Session = Depends(get_db)
):
    try:
        confession = services.ConfessionService.get_confession(db, confession_id)
        return confession
    except ValueError:
        raise HTTPException(status_code=404, detail="Confession Not Found!")

