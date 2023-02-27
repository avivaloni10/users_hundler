from sqlalchemy import Column, String
from config import Base


class User(Base):
    __tablename__ = "user"

    email = Column(String, primary_key=True)
    password = Column(String)
    phone_number = Column(String, unique=True)
    full_name = Column(String)
    car_model = Column(String, nullable=True)
    car_color = Column(String, nullable=True)
    plate_number = Column(String, nullable=True)
