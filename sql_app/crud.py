from sqlalchemy.orm import Session

from . import models, schemas

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return True

def get_Njournals_by_url(db: Session, url : str):
    return db.query(models.Njournal).filter(models.Njournal.url == url).first()


def create_Njournal(db: Session, journal: schemas.NjournalCreate):
    db_journal = models.Njournal(url = journal.url)
    db.add(db_journal)
    db.commit()
    db.refresh(db_journal)
    return True

def get_DailyRate_by_date(db: Session, date:str):
    return db.query(models.DailyRate).filter(models.DailyRate.date == date).first()

def create_DailyRate(db:Session, rate:schemas.DailyRateCreate):
    db_rate = models.DailyRate(date = rate.date)
    db.add(db_rate)
    db.commit()
    db.refresh(db_rate)
    return True

