import jwt
from fastapi import FastAPI

from routers import users_router
from config.db import engine, SessionLocal
from models import user

from fastapi import Depends, HTTPException

from sqlalchemy.orm import Session

from schemas.user_schemas import Response
from dal import user as user_crud

from fastapi.security import OAuth2PasswordRequestForm
import uuid

from fastapi.security import OAuth2PasswordBearer

user.Base.metadata.create_all(bind=engine)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/ping")
async def ping():
    return {"pong"}


# @app.post("/token")
# async def login(
#         db: Session = Depends(get_db),
#         form_data: OAuth2PasswordRequestForm = Depends(),
# ):
#     if not form_data or not form_data.username or not form_data.password:
#         raise HTTPException(status_code=400, detail="Please specify email and password")
#     current_user = user_crud.get_user_by_email(db, form_data.username)
#     if not current_user:
#         raise HTTPException(status_code=404, detail="User not found")
#     if current_user.password != form_data.password:
#         raise HTTPException(status_code=401, detail="Wrong password given")
#
#     jwt.encode(payload, SECRET_KEY, algorithm="HS256")
#     return {
#         "access_token": uuid.uuid5(namespace=uuid.NAMESPACE_X500, name=f"{form_data.username}{form_data.password}"),
#         "token_type": "bearer"
#     }


app.include_router(users_router.router, prefix="/users", tags=["users"])
