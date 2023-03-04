from sqlalchemy import Column, String
from config.db import Base


class User(Base):
    __tablename__ = "users"

    email = Column(String, primary_key=True, nullable=False)
    password = Column(String, nullable=False)
    phone_number = Column(String, unique=True, nullable=False)
    full_name = Column(String, nullable=False)
    car_model = Column(String, nullable=True)
    car_color = Column(String, nullable=True)
    plate_number = Column(String, nullable=True)
