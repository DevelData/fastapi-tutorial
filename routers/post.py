from typing import List

from fastapi import APIRouter, Response, status, HTTPException, Depends

from sqlalchemy.orm import Session

from app import models
from app.database import engine, get_db
from app.schemas import Post, PostCreate


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
    )


@router.get("/", response_model=List[Post])
def get_all_posts(db:Session=Depends(get_db)):
    #cursor.execute("SELECT * FROM posts")
    #posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Post)
def create_posts(post:PostCreate, db:Session=Depends(get_db)):
    #cursor.execute("""
    #               INSERT INTO posts (title, content, published)
    #               VALUES (%s, %s, %s)
    #               RETURNING *
    #               """,
    #               (post.title, post.content, post.published))
    #new_post = cursor.fetchone()
    #conn.commit()
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/{id}", response_model=Post)
def get_post(id:int, db:Session=Depends(get_db)):
    #cursor.execute("""SELECT * FROM posts WHERE id = %(id)s""", {"id": id})
    #post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} could not be found"
            )

    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db:Session=Depends(get_db)):
    #cursor.execute("""
    #               DELETE FROM posts
    #               WHERE id = %(id)s
    #               RETURNING *
    #               """,
    #               {"id": id})
    #deleted_post = cursor.fetchone()
    #conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)
    
    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id '{id}' does not exist")
    post.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=Post)
def update_post(id:int, post:PostCreate, db:Session=Depends(get_db)):
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
    
    if post_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id '{id}' does not exist")
    post_query.update(post.model_dump(), synchronize_session=False) # type: ignore
    db.commit()
    
    return post_query.first()