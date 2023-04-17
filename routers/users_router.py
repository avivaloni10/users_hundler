from fastapi import APIRouter, Depends, HTTPException
from config.db import SessionLocal
from sqlalchemy.orm import Session
from schemas.user_schemas import RequestUser, Response, RequestLogin
from dal import user as user_crud

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
async def create(request: RequestUser, db: Session = Depends(get_db)):
    user = user_crud.create_user(db, request.parameter)
    if not user:
        raise HTTPException(status_code=409, detail="Registration failed")
    return Response(code=200, status="OK", message="User created successfully").dict(exclude_none=True)


@router.get("/")
async def get(db: Session = Depends(get_db)):
    users = user_crud.get_users(db, 0, 100)
    return Response(code=200, status="OK", message="Users batch fetched successfully", result=users).dict(
        exclude_none=True)


@router.get("/{email}")
async def get_by_email(email: str, db: Session = Depends(get_db)):
    user = user_crud.get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return Response(code=200, status="OK", message="User fetched successfully", result=user).dict(exclude_none=True)


@router.put("/{email}")
async def update_by_email(email: str, request: RequestUser, db: Session = Depends(get_db)):
    user = user_crud.get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user = user_crud.update_user_by_email(db, email, request.parameter)
    return Response(code=200, status="OK", message="User updated successfully", result=user).dict(exclude_none=True)


@router.delete("/{email}")
async def delete_by_email(email: str, db: Session = Depends(get_db)):
    user = user_crud.get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user_crud.delete_user_by_email(db, email)
    return Response(code=200, status="OK", message="User deleted successfully").dict(exclude_none=True)


@router.post("/login")
async def login(request: RequestLogin, db: Session = Depends(get_db)):
    if not request or not request.parameter or not request.parameter.email or not request.parameter.password:
        raise HTTPException(status_code=400, detail="Please specify email and password")
    user = user_crud.get_user_by_email(db, request.parameter.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.password != request.parameter.password:
        raise HTTPException(status_code=401, detail="Wrong password given")
    return Response(code=200, status="OK", message="User logged in successfully", result=user).dict(exclude_none=True)
