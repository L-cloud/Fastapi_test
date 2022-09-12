from sqlalchemy import Column, Integer, String

from .database import Base


class Njournal(Base):
    __tablename__ = "Njournal"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, index=True)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)

class DailyRate(Base): 
    __tablename__ = "DailyRate"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(String, unique=True, index=True)