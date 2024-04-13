from typing import Dict, Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange



app = FastAPI()



class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating : Optional[int] = None


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


@app.get("/")
async def root():
    return {"message": "Welcome to my first API"}


@app.get("/posts")
def get_all_posts():
    return {"data": my_posts}


@app.post("/posts")
def create_posts(post:Post):
    post_dict = post.model_dump()
    post_dict["id"] = randrange(0, 10**8)
    my_posts.append(post_dict)
    return {"data": post_dict}


@app.get("/posts/{id}")
def get_post(id:int):
    post = find_post(id)
    return {"post_detail": post}