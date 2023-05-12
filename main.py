from fastapi import FastAPI

from config.db import engine
from models import user
from routers import users_router

user.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/ping")
async def ping():
    return {"pong"}


app.include_router(users_router.router, prefix="/users", tags=["users"])
