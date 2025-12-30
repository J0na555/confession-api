from sqlalchemy.orm import Session
from sqlalchemy import func
from app import models, schemas


class VoteService:
    @staticmethod
    def upvote_comment(db: Session, comment_id: str, voter_ip: str):
        """Upvote a comment. If already upvoted, removes the vote. If downvoted, changes to upvote."""
        comment = db.query(models.Comment).filter(
            models.Comment.id == comment_id
        ).first()
        if not comment:
            raise ValueError(f"Comment with id {comment_id} not found")
        
        # Check if vote already exists
        existing_vote = db.query(models.Vote).filter(
            models.Vote.comment_id == comment_id,
            models.Vote.voter_ip == voter_ip
        ).first()
        
        if existing_vote:
            if existing_vote.vote_value == 1:
                # Already upvoted, remove the vote
                db.delete(existing_vote)
                db.commit()
                return {"action": "removed", "vote_value": 0}
            else:
                # Was downvoted, change to upvote
                existing_vote.vote_value = 1
                db.commit()
                db.refresh(existing_vote)
                return {"action": "changed_to_upvote", "vote_value": 1}
        else:
            # New upvote
            vote = models.Vote(
                comment_id=comment_id,
                voter_ip=voter_ip,
                vote_value=1
            )
            db.add(vote)
            db.commit()
            db.refresh(vote)
            return {"action": "upvoted", "vote_value": 1}
    
    @staticmethod
    def downvote_comment(db: Session, comment_id: str, voter_ip: str):
        """Downvote a comment. If already downvoted, removes the vote. If upvoted, changes to downvote."""
        comment = db.query(models.Comment).filter(
            models.Comment.id == comment_id
        ).first()
        if not comment:
            raise ValueError(f"Comment with id {comment_id} not found")
        
        # Check if vote already exists
        existing_vote = db.query(models.Vote).filter(
            models.Vote.comment_id == comment_id,
            models.Vote.voter_ip == voter_ip
        ).first()
        
        if existing_vote:
            if existing_vote.vote_value == -1:
                # Already downvoted, remove the vote
                db.delete(existing_vote)
                db.commit()
                return {"action": "removed", "vote_value": 0}
            else:
                # Was upvoted, change to downvote
                existing_vote.vote_value = -1
                db.commit()
                db.refresh(existing_vote)
                return {"action": "changed_to_downvote", "vote_value": -1}
        else:
            # New downvote
            vote = models.Vote(
                comment_id=comment_id,
                voter_ip=voter_ip,
                vote_value=-1
            )
            db.add(vote)
            db.commit()
            db.refresh(vote)
            return {"action": "downvoted", "vote_value": -1}
    
    @staticmethod
    def get_vote_counts(db: Session, comment_id: str):
        """Get upvote and downvote counts for a comment."""
        upvotes = db.query(func.count(models.Vote.id)).filter(
            models.Vote.comment_id == comment_id,
            models.Vote.vote_value == 1
        ).scalar() or 0
        
        downvotes = db.query(func.count(models.Vote.id)).filter(
            models.Vote.comment_id == comment_id,
            models.Vote.vote_value == -1
        ).scalar() or 0
        
        return {
            "upvotes": upvotes,
            "downvotes": downvotes,
            "score": upvotes - downvotes
        }
    
    @staticmethod
    def get_user_vote(db: Session, comment_id: str, voter_ip: str):
        """Get the current vote status for a user on a comment."""
        vote = db.query(models.Vote).filter(
            models.Vote.comment_id == comment_id,
            models.Vote.voter_ip == voter_ip
        ).first()
        
        if vote:
            return vote.vote_value
        return 0
