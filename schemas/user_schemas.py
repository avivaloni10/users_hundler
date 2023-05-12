from typing import Optional, Generic, TypeVar
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel

T = TypeVar('T')


class LoginSchema(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None


class UserSchema(BaseModel):
    email: str
    password: str
    phone_number: str
    full_name: str
    car_model: Optional[str] = None
    car_color: Optional[str] = None
    plate_number: Optional[str] = None

    class Config:
        orm_mode = True


class UserUpdateSchema(BaseModel):
    full_name: Optional[str] = None
    car_model: Optional[str] = None
    car_color: Optional[str] = None
    plate_number: Optional[str] = None

    class Config:
        orm_mode = True


class Request(GenericModel, Generic[T]):
    parameter: Optional[T] = Field(...)


class RequestLogin(BaseModel):
    parameter: LoginSchema = Field(...)


class RequestUser(BaseModel):
    parameter: UserSchema = Field(...)


class RequestUserUpdate(BaseModel):
    parameter: UserUpdateSchema = Field(...)


class Response(GenericModel, Generic[T]):
    code: int
    status: str
    message: str
    result: Optional[T]


class Token(BaseModel):
    email: str
