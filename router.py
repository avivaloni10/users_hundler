from fastapi import APIRouter, Depends
from config import SessionLocal
from sqlalchemy.orm import Session
from schemas import RequestUser, Response
import crud

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
async def create(request: RequestUser, db: Session = Depends(get_db)):
    crud.create_user(db, request.parameter)
    return Response(code=200, status="OK", message="User created successfully").dict(exclude_none=True)


@router.get("/")
async def get(db: Session = Depends(get_db)):
    user = crud.get_users(db, 0, 100)
    return Response(code=200, status="OK", message="Users batch fetched successfully", result=user).dict(
        exclude_none=True)


@router.get("/{email}")
async def get_by_email(email: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email)
    return Response(code=200, status="OK", message="User fetched successfully", result=user).dict(exclude_none=True)


@router.put("/{email}")
async def update_by_email(email: str, request: RequestUser, db: Session = Depends(get_db)):
    user = crud.update_user_by_email(db, email, request.parameter)
    return Response(code=200, status="OK", message="User updated successfully", result=user).dict(exclude_none=True)


@router.delete("/{email}")
async def update_by_email(email: str, db: Session = Depends(get_db)):
    crud.delete_user_by_email(db, email)
    return Response(code=200, status="OK", message="User deleted successfully").dict(exclude_none=True)
