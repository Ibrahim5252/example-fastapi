from fastapi import status, HTTPException, Depends, APIRouter
from typing import List, Optional
from ..database import engine, get_db
from sqlalchemy.orm import Session
from .. import models, pydantric_schemas, oauth2
from sqlalchemy import func



#! =============================================================================================
#? ============================== POST SECTION =================================================
#! =============================================================================================
#? This section handles POST REALATED WORK


router = APIRouter(
    prefix = '/posts', #!<-we use this so we can avoid writing same thing "/posts" in every decorater and write once and just leave "/" or "/{id}".
    tags = ['Posts']   #!<-this done for fastAPI docs so we can have all posts in seperate section rather than having it in default section
)

#! GETS ALL POSTS.#########################################################################################
@router.get("/", response_model=List[pydantric_schemas.PostOut])  #! have to use list for response_model it will not work as it work for other so imported list from typing
def get_posts(db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_currrnt_user), limit: int = 10, skip: int = 0,
              search: Optional[str] = ""):
        # cursor.execute("""SELECT * FROM posts """)
        # posts = cursor.fetchall()
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all() #! it's for to turn post private like insta.
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() #! it's for public like insta
    
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
#!actual query performed in sql <-^-> select  posts.* , count(votes.post_id) as votes from posts left join votes on posts.id = votes.post_id where posts.id = 23 group by posts.id;
    return  posts






#! GET 1 POST VIA ID.#########################################################################################
@router.get("/{id}", response_model=pydantric_schemas.PostOut)
def get_post_via_id(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_currrnt_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, str(id))
    # post = cursor.fetchone()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} was not found.")   
    return post


#! CREATE POST.#########################################################################################
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=pydantric_schemas.Post)
def create_post(post: pydantric_schemas.CreatePost, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_currrnt_user)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES(%s, %s, %s) RETURNING * """,(post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # con.commit()
   
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


#! DELETE POST VIA ID.#########################################################################################
@router.delete("/{id}")
def delete_post_via_id(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_currrnt_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id)))
    # post = cursor.fetchone()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    own = post_query.first()

    if own is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} does not exist.")

    if own.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not Authorized to perform requested task.")

    post_query.delete(synchronize_session=False)
    db.commit()
    return {"Message" : "Post deleted succesfully."}


#! UPDATE POST VIA ID#########################################################################################
@router.put("/{id}", response_model=pydantric_schemas.Post)
def update_post(id: int, post: pydantric_schemas.CreatePost, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_currrnt_user)):

    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()

    query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = query.first()

   

    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} does not exist.")

    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not Authorized to perform requested task.")

    post_dict = post.model_dump()
    query.update(post_dict, synchronize_session=False)  # type: ignore
    
    db.commit()
    
    return  query.first()