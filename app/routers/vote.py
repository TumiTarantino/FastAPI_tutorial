from multiprocessing import synchronize

from fastapi import FastAPI, HTTPException, Response, status, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, database, oauth2, models

router = APIRouter(
    prefix="/vote",
    tags=['Votes']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id) #type: ignore
    found_vote = vote_query.first()

    if (vote.vote_dir == 1):
       if found_vote:
           raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                               detail="Already voted on post")
       new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
       db.add(new_vote)
       db.commit()
       return {"message" : "successfully voted on post"}
    else:
        if not found_vote:
           raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message":"successfully deleted vote"}