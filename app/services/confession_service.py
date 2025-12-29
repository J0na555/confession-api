from sqlalchemy.orm import Session
from app import models, schemas

class ConfessionService:
    @staticmethod
    def create_confession(db: Session, confession: schemas.ConfessionCreate):
        # Convert Pydantic model to sqlalchemy models
        db_confession = models.Confession(
            confession=confession.confession,
        )
        db.add(db_confession)
        db.commit()
        db.refresh(db_confession)
        return db_confession
    
    @staticmethod
    def get_confession(db: Session, confession_id: str):
        confession = db.query(models.Confession).filter(
            models.Confession.id == confession_id
        ).first()
        if not confession:
            raise ValueError(f"Confession with id {confession_id} not found")
        return confession
    
    @staticmethod
    def get_confessions(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Confession).order_by(
            models.Confession.created_at.desc()
        ).offset(skip).limit(limit).all()
    
    # @staticmethod
    # def delete_confession(db: Session, confession_id: int):
    #     confession = db.query(models.Confession).filter(
    #         models.Confession.id == confession_id
    #     ).first()
    #     if confession:
    #         db.delete(confession)
    #         db.commit()
    #     return confession