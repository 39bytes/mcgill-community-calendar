from sqlalchemy import Column, Integer, String
from codejamapp.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(50), unique = True, nullable = False)
    password = Column(String(256), nullable = False)

    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password