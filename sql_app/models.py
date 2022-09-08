from sqlalchemy import Column, Integer, String

from .database import Base


class Njournal(Base):
    __tablename__ = "Njournal"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, index=True)


class DailyRate(Base): # 문제가 있음 이거... 장 안 여는 날이랑 여는 날 비교해서 중복 어떻게 처리할지 체크 해야함
    __tablename__ = "DailyRate"
    id = Column(Integer, primary_key=True, index=True)
    day = Column(String, unique=True, index=True)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)