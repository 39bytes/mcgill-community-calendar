from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
import datetime
from sqlalchemy.orm import relationship
from codejamapp.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(50), unique = True, nullable = False)
    password = Column(String(256), nullable = False)
    description = Column(Text, nullable=True)
    pfp_filename = Column(String(256), nullable=True)

    events = relationship("Event", back_populates="creator")

    def __init__(self, name: str, email: str, password: str, pfp_filename="" , description=""):
        self.name = name
        self.email = email
        self.password = password
        self.pfp_filename = pfp_filename
        self.description = description

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
    image_filename = Column(String(256))

    def __init__(self, name: str, creator_id: int, description: str, location: str,
                 start_time: datetime.datetime, tags="", image_filename=""):
        self.name = name
        self.creator_id = creator_id
        self.description = description
        self.location = location
        self.start_time = start_time
        self.tags = tags
        self.image_filename=image_filename

VALID_TAGS = {
    "Club" : "bg-red-500",
    "Workshop": "bg-green-500",
    "Fundraiser": "bg-pink-500",
    "Volunteer": "bg-yellow-500",
    "Science": "bg-blue-500",
    "Engineering": "bg-purple-500"
}

