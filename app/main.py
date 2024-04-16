from typing import List
from random import randrange
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app import models
from app.database import engine, get_db
from app.schemas import Post, PostCreate, UserCreate, UserOut



pwd_context = CryptContext(schemes="bcrypt", deprecated="auto")
models.Base.metadata.create_all(bind=engine)
app = FastAPI()



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


@app.get("/posts", response_model=List[Post])
def get_all_posts(db:Session=Depends(get_db)):
    #cursor.execute("SELECT * FROM posts")
    #posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=Post)
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


@app.get("/posts/{id}", response_model=Post)
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


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
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


@app.put("/posts/{id}", response_model=Post)
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


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user:UserCreate, db:Session=Depends(get_db)):
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
