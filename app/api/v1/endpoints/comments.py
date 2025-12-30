from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app import schemas, services

router = APIRouter()

@router.post("/", response_model=schemas.Comment)
def create_comment(
    comment: schemas.CommentCreate,
    db: Session = Depends(get_db)
):
    try:
        return services.CommentService.create_comment(db, comment)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/confession/{confession_id}", response_model=List[schemas.Comment])
def get_comments_by_confession(
    confession_id: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    try:
        comments = services.CommentService.get_comments_by_confession(
            db, confession_id, skip, limit
        )
        return comments
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{comment_id}", response_model=schemas.Comment)
def get_comment(
    comment_id: str,
    db: Session = Depends(get_db)
):
    try:
        comment = services.CommentService.get_comment(db, comment_id)
        return comment
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
