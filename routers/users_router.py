import uuid

from fastapi import APIRouter, Depends, HTTPException

from config.db import SessionLocal
from sqlalchemy.orm import Session

from schemas.user_schemas import RequestUser, Response
from dal import user as user_crud

from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.exc import IntegrityError

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def validate_token(db: Session, token: str) -> None:
    try:
        if user_crud.get_user_by_token(db, token):
            return
        raise HTTPException(status_code=401, detail="Unauthorized")
    except IntegrityError as ie:
        print(ie)
        raise HTTPException(status_code=401, detail="Unauthorized")


@router.post("/")
async def create(
        request: RequestUser,
        db: Session = Depends(get_db),
):
    user = user_crud.create_user(db, request.parameter, str(uuid.uuid5(
        namespace=uuid.NAMESPACE_X500, name=f"{request.parameter.email}{request.parameter.password}")
    ))
    if not user:
        raise HTTPException(status_code=409, detail="Registration failed")
    return Response(
        code=200,
        status="OK",
        message="User created successfully",
    ).dict(exclude_none=True)


@router.get("/")
async def get(
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_scheme),
):
    await validate_token(db, token)

    users = user_crud.get_users(db, 0, 100)
    return Response(code=200, status="OK", message="Users batch fetched successfully", result=users).dict(
        exclude_none=True)


@router.get("/validate_token")
async def is_token_valid(
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_scheme),
):
    await validate_token(db, token)

    return Response(code=200, status="OK", message="Token is valid", result={"is_valid": True}).dict(
        exclude_none=True)


@router.get("/{email}")
async def get_by_email(
        email: str,
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_scheme),
):
    await validate_token(db, token)

    user = user_crud.get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return Response(code=200, status="OK", message="User fetched successfully", result=user).dict(exclude_none=True)


@router.put("/{email}")
async def update_by_email(
        email: str,
        request: RequestUser,
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_scheme),
):
    await validate_token(db, token)

    user = user_crud.get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user = user_crud.update_user_by_email(db, email, request.parameter)
    return Response(code=200, status="OK", message="User updated successfully", result=user).dict(exclude_none=True)


@router.delete("/{email}")
async def delete_by_email(
        email: str,
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_scheme),
):
    await validate_token(db, token)

    user = user_crud.get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user_crud.delete_user_by_email(db, email)
    return Response(code=200, status="OK", message="User deleted successfully").dict(exclude_none=True)
