from typing import Dict, Optional
from random import randrange
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from app import models
from app.database import engine, get_db



models.Base.metadata.create_all(bind=engine)
app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True

# This caused a bug - changing to the correct password did not establish
# normal flow.
# while True: 
try:
    conn = psycopg2.connect(
        host="localhost",
        database="fastapi",
        user="postgres",
        password="password",
        cursor_factory=RealDictCursor
        )
    cursor = conn.cursor()
    print("Connection to database was successful!")
    #break
except Exception as err:
    print(f"Connection attempt to database failed. Error: {err}")
    #time.sleep(1.5)


my_posts = [
    {
        "title": "title of post 1",
        "content": "content of post 1",
        "id": 1
    },
    {
        "title": "favourite foods",
        "content": "I like pizza",
        "id": 2
    }
]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
        

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i


@app.get("/")
async def root():
    return {"message": "Welcome to my first API"}


@app.get("/sqlalchemy")
def test_posts(db:Session=Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.get("/posts")
def get_all_posts(db:Session=Depends(get_db)):
    #cursor.execute("SELECT * FROM posts")
    #posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post:Post):
    cursor.execute("""
                   INSERT INTO posts (title, content, published)
                   VALUES (%s, %s, %s)
                   RETURNING *
                   """,
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}


@app.get("/posts/{id}")
def get_post(id:int):
    cursor.execute("""SELECT * FROM posts WHERE id = %(id)s""", {"id": id})
    post = cursor.fetchone()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} could not be found"
            )

    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    cursor.execute("""
                   DELETE FROM posts
                   WHERE id = %(id)s
                   RETURNING *
                   """,
                   {"id": id})
    deleted_post = cursor.fetchone()
    conn.commit()
    
    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id '{id}' does not exist")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id:int, post:Post):
    cursor.execute("""
                    UPDATE posts
                    SET
                        title = %(title)s,
                        content = %(content)s,
                        published = %(published)s
                    WHERE
                        id = %(id)s
                    RETURNING *
                   """,
                   {
                       "title": post.title,
                       "content": post.content,
                       "published": post.published,
                       "id": id
                   })
    updated_post = cursor.fetchone()
    conn.commit()
    
    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id '{id}' does not exist")
    
    return {"data": updated_post}