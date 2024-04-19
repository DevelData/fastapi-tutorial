from typing import List

from fastapi import APIRouter, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app import models, oauth2
from app.database import get_db
from app.schemas import Post, PostCreate, PostOut, UserOut


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
    )


@router.get("/", response_model=List[PostOut])
def get_all_posts(
    db:Session=Depends(get_db),
    current_user:UserOut=Depends(oauth2.get_current_user),
    limit:int=10,
    skip:int=0,
    search:str=""
    ):
    #cursor.execute("SELECT * FROM posts")
    #posts = cursor.fetchall()
    results_object =  db.query(models.Post, func.count(models.Vote.post_id).label("votes"))\
                                                     .join(models.Vote,
                                                           models.Post.id == models.Vote.post_id,
                                                           isouter=True)\
                                                     .group_by(models.Post.id)\
                                                     .filter(models.Post.title.contains(search))\
                                                     .limit(limit=limit)\
                                                     .offset(offset=skip).all()
    results = list(map(lambda x: x._mapping, results_object))

    return results


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Post)
def create_posts(
    post:PostCreate,
    db:Session=Depends(get_db),
    current_user:UserOut=Depends(oauth2.get_current_user)
    ):
    #cursor.execute("""
    #               INSERT INTO posts (title, content, published)
    #               VALUES (%s, %s, %s)
    #               RETURNING *
    #               """,
    #               (post.title, post.content, post.published))
    #new_post = cursor.fetchone()
    #conn.commit()
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/{id}", response_model=PostOut)
def get_post(
    id:int,
    db:Session=Depends(get_db),
    current_user:UserOut=Depends(oauth2.get_current_user)
    ):
    #cursor.execute("""SELECT * FROM posts WHERE id = %(id)s""", {"id": id})
    #post = cursor.fetchone()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes"))\
                                           .join(models.Vote,
                                                 models.Post.id == models.Vote.post_id,
                                                 isouter=True)\
                                           .group_by(models.Post.id)\
                                           .filter(models.Post.id == id)\
                                           .first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} could not be found"
            )

    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id:int,
    db:Session=Depends(get_db),
    current_user:UserOut=Depends(oauth2.get_current_user)):
    #cursor.execute("""
    #               DELETE FROM posts
    #               WHERE id = %(id)s
    #               RETURNING *
    #               """,
    #               {"id": id})
    #deleted_post = cursor.fetchone()
    #conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id '{id}' does not exist")
    
    if post.owner_id != current_user.id: # type: ignore
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action."
            )

    post_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=Post)
def update_post(
    id:int,
    post:PostCreate,
    db:Session=Depends(get_db),
    current_user:UserOut=Depends(oauth2.get_current_user)
    ):
    #cursor.execute("""
    #                UPDATE posts
    #                SET
    #                    title = %(title)s,
    #                    content = %(content)s,
    #                    published = %(published)s
    #                WHERE
    #                    id = %(id)s
    #                RETURNING *
    #               """,
    #               {
    #                   "title": post.title,
    #                   "content": post.content,
    #                   "published": post.published,
    #                   "id": id
    #               })
    #updated_post = cursor.fetchone()
    #conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_from_db = post_query.first()
    
    if post_from_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id '{id}' does not exist")
    
    if post_from_db.owner_id != current_user.id: # type: ignore
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action."
            )

    post_query.update(post.model_dump(), synchronize_session=False) # type: ignore
    db.commit()
    
    return post_query.first()