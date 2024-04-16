from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
from app import models
from app.database import engine
from routers import post, user



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


app.include_router(post.router)
app.include_router(user.router)


@app.get("/")
async def root():
    return {"message": "Welcome to my first API"}