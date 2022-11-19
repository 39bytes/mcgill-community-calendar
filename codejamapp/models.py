from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
import datetime
from sqlalchemy.orm import relationship
from codejamapp.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(50), unique = True, nullable = False)
    password = Column(String(256), nullable = False)

    events = relationship("Event", back_populates="creator")

    def __init__(self, username: str, email: str, password: str):
        self.username = username
        self.email = email
        self.password = password

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    description = Column(Text)
    location = Column(String(256))
    start_time = Column(DateTime(timezone=True))
    tags = Column(Text, nullable=True) # A comma separated list of tags
    creator_id = Column(Integer, ForeignKey("users.id"))
    creator = relationship("User", back_populates="events")

    def __init__(self, name: str, creator_id: int, description: str, location: str, 
                 start_time: datetime.datetime, tags=""):
        self.name = name
        self.creator_id = creator_id
        self.description = description
        self.location = location
        self.start_time = start_time
        self.tags = tags

