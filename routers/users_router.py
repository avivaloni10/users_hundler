from datetime import timedelta, datetime
from functools import lru_cache

import jwt
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from config.auth import SECRET_KEY_LOCATION
from config.db import SessionLocal
from dal import user as user_crud
from schemas.user_schemas import RequestUser, Response, Token, RequestUserUpdate

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@lru_cache
def get_secret_key() -> str:
    with open(SECRET_KEY_LOCATION, mode="r") as f:
        return f.read()


async def validate_token(token: str, secret_key: str) -> dict:
    try:
        # Attempt to decode and verify the JWT token using the secret key
        return jwt.decode(token, secret_key, algorithms=['HS256'])
    except jwt.exceptions.DecodeError:
        # If the token cannot be decoded (e.g. due to an invalid signature or format), raise an error
        raise HTTPException(status_code=401, detail='Invalid JWT token')
    except jwt.exceptions.ExpiredSignatureError:
        # If the token has expired, raise an error
        raise HTTPException(status_code=401, detail='JWT token has expired')


async def validated_token(
        token: str = Depends(oauth2_scheme),
        secret_key: str = Depends(get_secret_key)
) -> Token:
    return Token(**await validate_token(token, secret_key))


@router.post("/")
async def create(
    request: RequestUser,
    db: Session = Depends(get_db),
    secret_key=Depends(get_secret_key),
):
    try:
        u = user_crud.get_user_by_email(db, request.parameter.email)
        if u:
            raise HTTPException(status_code=400, detail="User already exist")
        user = user_crud.create_user(db=db, user=request.parameter)
    except IntegrityError as ie:
        print(ie)
        raise HTTPException(status_code=400, detail="DB constraint reached")
    if not user:
        raise HTTPException(status_code=409, detail="Registration failed")

    t = get_token(request.parameter.email, secret_key)
    return Response(
        code=200,
        status="OK",
        message="User created successfully",
        result={"token": t}
    ).dict(exclude_none=True)


@router.get("/")
async def get(
        db: Session = Depends(get_db),
        _=Depends(validated_token)
):

    users = user_crud.get_users(db, 0, 100)
    return Response(code=200, status="OK", message="Users batch fetched successfully", result=users).dict(
        exclude_none=True)


@router.get("/validate_token")
async def is_token_valid(
    tkn: Token = Depends(validated_token)
):
    return Response(code=200, status="OK", message="Token is valid", result={"is_valid": True, "token": tkn.dict()}).dict(
        exclude_none=True)


@router.get("/{email}")
async def get_by_email(
        email: str,
        db: Session = Depends(get_db),
        _=Depends(validated_token)
):

    user = user_crud.get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return Response(code=200, status="OK", message="User fetched successfully", result=user).dict(exclude_none=True)


@router.put("/{email}")
async def update_by_email(
        email: str,
        request: RequestUserUpdate,
        db: Session = Depends(get_db),
        _=Depends(validated_token)
):

    user = user_crud.get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user = user_crud.update_user_by_email(db, email, request.parameter)
    return Response(code=200, status="OK", message="User updated successfully", result=user).dict(exclude_none=True)


@router.delete("/{email}")
async def delete_by_email(
        email: str,
        db: Session = Depends(get_db),
        _=Depends(validated_token)
):

    user = user_crud.get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user_crud.delete_user_by_email(db, email)
    return Response(code=200, status="OK", message="User deleted successfully").dict(exclude_none=True)


@router.post("/login")
@router.post("/token")
async def login(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
    secret_key=Depends(get_secret_key),
):
    if not form_data or not form_data.username or not form_data.password:
        raise HTTPException(status_code=400, detail="Please specify email and password")
    current_user = user_crud.get_user_by_email(db, form_data.username)
    if not current_user or not current_user.check_password(form_data.password):
        raise HTTPException(status_code=401, detail="Wrong email or password given")

    token = get_token(form_data.username, secret_key)
    return {
        "access_token": token,
        "token_type": "bearer"
    }


def get_token(username: str, secret_key: str) -> str:
    payload = Token(email=username).dict()
    expiry_time = datetime.utcnow() + timedelta(hours=1)
    token = jwt.encode({'exp': expiry_time, **payload}, secret_key, algorithm='HS256')
    return token
