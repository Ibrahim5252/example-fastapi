from fastapi import status, HTTPException, Depends, APIRouter
from typing import List, Optional
from ..database import engine, get_db
from sqlalchemy.orm import Session
from .. import models, pydantric_schemas, oauth2

#! =============================================================================================
#? ============================== VOTE SECTION =================================================
#! =============================================================================================
#? This section handles VOTE REALATED WORK


router = APIRouter(
    prefix = '/vote', #!<-we use this so we can avoid writing same thing "/posts" in every decorater and write once and just leave "/" or "/{id}".
    tags = ['Vots']   #!<-this done for fastAPI docs so we can have all posts in seperate section rather than having it in default section
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: pydantric_schemas.Vote, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_currrnt_user)):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {vote.post_id} does not exists.")

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user with {current_user.id} has already voted on post with id {vote.post_id}.")
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"Message" : "succesfully added vote."}
    
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="vote does not exists.")
        
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"Message" : "succesfully deleted vote."}


    
         