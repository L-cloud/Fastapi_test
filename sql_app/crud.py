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
    db_item = models.Njournal(url = journal.url)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return True

