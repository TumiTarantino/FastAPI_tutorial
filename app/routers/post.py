from .. import models, schemas, utils, oauth2
from fastapi import HTTPException, Response, status, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
# One route uses this, maybe there's a better way?
from typing import List

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/{id}",response_model=schemas.Post)
def get_post(id: int, db: Session= Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    #Commented because of ORM, don't delete
    #cursor.execute("""SELECT * FROM posts WHERE id = %s """,(id,))
    #post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first() #type: ignore

    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"post with {id} is not found")
    return post

@router.get("/",response_model=List[schemas.Post])
def get_posts(db: Session= Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10):
    #Commented out since we are using ORMs now, don't delete
    #cursor.execute("""SELECT * FROM posts """)
    #posts = cursor.fetchall()

    #ORMS way
    posts = db.query(models.Post).limit(limit).all() #type: ignore
    return posts

#Added Oauth2 stuff to verify user
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post:schemas.PostBase,db: Session= Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #Try to sanitize the statement(NO SQL INJECTION PLZ)[Commented out because ORM, don't delete]
    #cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    #                (post.title, post.content, post.published))
    #new_post = cursor.fetchone()#Saves the executed result in a variable, fetchall gets the result of the execute
    #conn.commit()# Saves changes to the actual database

    #temp checks
    # type: ignore pylance issue but probably because of schemas.py tokendata or something related

    #ORM way:
    new_post = models.Post(owner_id=current_user.id,**post.dict())#use post.model_dump after tutorial #type: ignore
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db: Session= Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    #Replaced with ORM logic, don't delete
    #cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """,(id,))
    #deleted_post = cursor.fetchone()
    #conn.commit() (put after the exception check but it commented out now)
    post = db.query(models.Post).filter(models.Post.id == id).first() #type: ignore
    print(post)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist"
        )
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not authorized to perform requested action"
        )
    #post.delete(synchronize_session=False)
    db.delete(post)
    db.commit()
    #Apparently if you delete data or 204 is the status code, you don't want to return anything
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostBase,db: Session= Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    #Replaced with ORM, don't delete
    #cursor.execute("""UPDATE posts SET title= %s, content= %s, published= %s WHERE id = %s RETURNING * """,
    #              (post.title, post.content, post.published, id,))
    #updated_post = cursor.fetchone()
    #conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)#type: ignore
    post = post_query.first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist"
        )
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not authorized to perform requested action"
        )
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    
    return post_query.first()