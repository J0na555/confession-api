from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.db.database import get_db
from app import services

router = APIRouter()


def get_client_ip(request: Request) -> str:
    """Extract client IP address from request."""
    # Check for forwarded IP (if behind proxy)
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    
    # Check for real IP
    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        return real_ip
    
    # Fallback to direct client
    if request.client:
        return request.client.host
    
    return "unknown"


@router.post("/comments/{comment_id}/upvote")
def upvote_comment(
    comment_id: str,
    request: Request,
    db: Session = Depends(get_db)
):
    """Upvote a comment. If already upvoted, removes the vote."""
    try:
        voter_ip = get_client_ip(request)
        result = services.VoteService.upvote_comment(db, comment_id, voter_ip)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/comments/{comment_id}/downvote")
def downvote_comment(
    comment_id: str,
    request: Request,
    db: Session = Depends(get_db)
):
    """Downvote a comment. If already downvoted, removes the vote."""
    try:
        voter_ip = get_client_ip(request)
        result = services.VoteService.downvote_comment(db, comment_id, voter_ip)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/comments/{comment_id}/votes")
def get_comment_votes(
    comment_id: str,
    db: Session = Depends(get_db)
):
    """Get vote counts for a comment."""
    try:
        vote_counts = services.VoteService.get_vote_counts(db, comment_id)
        return vote_counts
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/comments/{comment_id}/my-vote")
def get_my_vote(
    comment_id: str,
    request: Request,
    db: Session = Depends(get_db)
):
    """Get the current vote status for the requesting IP on a comment."""
    try:
        voter_ip = get_client_ip(request)
        vote_value = services.VoteService.get_user_vote(db, comment_id, voter_ip)
        return {"vote_value": vote_value}  # 1 for upvote, -1 for downvote, 0 for no vote
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
