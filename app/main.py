from fastapi import FastAPI
from app.database import engine
from app.routers import auth, post, user, vote


# from app import models
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
async def root():
    return {"message": "Welcome to my first API"}