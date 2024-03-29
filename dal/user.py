from typing import Optional

from sqlalchemy.orm import Session
from models.user import User
from schemas.user_schemas import UserSchema, UserUpdateSchema


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def get_user_by_token(db: Session, token: str):
    return db.query(User).filter(User.token == token).first()


def create_user(db: Session, user: UserSchema):
    new_user = User(
        email=user.email,
        password=None,
        phone_number=user.phone_number,
        full_name=user.full_name,
        car_model=user.car_model,
        car_color=user.car_color,
        plate_number=user.plate_number,
    )
    new_user.set_password(user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def delete_user_by_email(db: Session, email: str):
    user = get_user_by_email(db=db, email=email)
    db.delete(user)
    db.commit()


def update_user_by_email(db: Session, email: str, user: UserUpdateSchema):
    old_user = get_user_by_email(db=db, email=email)

    old_user.password = user.password if user.password else old_user.password
    old_user.full_name = user.full_name if user.full_name else old_user.full_name
    old_user.car_model = user.car_model if user.car_model else old_user.car_model
    old_user.car_color = user.car_color if user.car_color else old_user.car_color
    old_user.plate_number = user.plate_number if user.plate_number else old_user.plate_number

    db.commit()
    db.refresh(old_user)
    return old_user
