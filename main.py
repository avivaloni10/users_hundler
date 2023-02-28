from fastapi import FastAPI

from routers import users_router
from config.db import engine
from models import user

user.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/ping")
async def ping():
    return {"pong"}

app.include_router(users_router.router, prefix="/users", tags=["users"])
