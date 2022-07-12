from pyexpat import model
from typing import Dict
from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils, oauth2
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.get("/", status_code=status.HTTP_201_CREATED)
def get_vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: Dict = Depends(oauth2.get_current_user)):

    post_found = db.query(models.Post).filter(models.Post.id == vote.post_id).first()

    if not post_found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {vote.post_id} does not exist.")
    
    voted_query = db.query(models.Vote).filter(models.Vote.user_id == current_user.id, models.Vote.post_id == vote.post_id)
    voted = voted_query.first()

    if voted:
        voted_query.delete(synchronize_session=False)
        db.commit()
        return {'message': "Unvoted successfully!"}

    new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
    db.add(new_vote)
    db.commit()
    return {'message': "Voted successfully!"}
    
