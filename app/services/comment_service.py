from sqlalchemy.orm import Session
from app import models, schemas

class CommentService:
    @staticmethod
    def create_comment(db: Session, comment: schemas.CommentCreate):
        # Verify that the confession exists
        confession = db.query(models.Confession).filter(
            models.Confession.id == comment.confession_id
        ).first()
        if not confession:
            raise ValueError(f"Confession with id {comment.confession_id} not found")
        
        # Convert Pydantic model to sqlalchemy model
        db_comment = models.Comment(
            confession_id=comment.confession_id,
            comment=comment.comment,
        )
        db.add(db_comment)
        db.commit()
        db.refresh(db_comment)
        return db_comment
    
    @staticmethod
    def get_comment(db: Session, comment_id: str):
        comment = db.query(models.Comment).filter(
            models.Comment.id == comment_id
        ).first()
        if not comment:
            raise ValueError(f"Comment with id {comment_id} not found")
        return comment
    
    @staticmethod
    def get_comments_by_confession(db: Session, confession_id: str, skip: int = 0, limit: int = 100):
        # Verify that the confession exists
        confession = db.query(models.Confession).filter(
            models.Confession.id == confession_id
        ).first()
        if not confession:
            raise ValueError(f"Confession with id {confession_id} not found")
        
        return db.query(models.Comment).filter(
            models.Comment.confession_id == confession_id
        ).order_by(
            models.Comment.created_at.asc()
        ).offset(skip).limit(limit).all()
