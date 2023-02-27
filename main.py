from fastapi import FastAPI

from routers import users_router
from config import engine
from models import user

user.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

app.include_router(router.router, prefix="/users", tags=["users"])
