import uuid

import bcrypt
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

    def set_password(self, password: str):
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
        self.password = password_hash.decode('utf-8')

    def check_password(self, password: str):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
