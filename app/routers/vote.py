from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session

from app import models, oauth2
from app.database import get_db
from app.schemas import UserOut, Vote


router = APIRouter(
    prefix="/votes",
    tags=["Vote"]
    )


@router.post("/", status_code=status.HTTP_201_CREATED)
def add_vote(
    vote:Vote,
    db:Session=Depends(get_db),
    current_user:UserOut=Depends(oauth2.get_current_user)
    ):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
     
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with {vote.post_id} does not exist."
            )

    vote_query = db.query(models.Vote).filter(
            models.Vote.post_id == vote.post_id,
            models.Vote.user_id == current_user.id
            )
    found_vote = vote_query.first()

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User {current_user.id} has already voted on post {vote.post_id}."
                )
        
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Successfully added vote!"}
    
    else:
        if found_vote is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vote does not exist."
                )
        
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Successfully deleted vote!"}