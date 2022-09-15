from fastapi import FastAPI,Request,Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import Union
from sqlalchemy.orm import Session
from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
import os

models.Base.metadata.create_all(bind=engine)

# Dependency

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static") 

@app.get("/", response_class=HTMLResponse)
async def main(request: Request,message:Union[None, str] = None):
    return templates.TemplateResponse('main.html',{"request" : request,"message" :message})

@app.post("/add")
async def add_email(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    print(user,type(user), db, type(db))
    if db_user:
        return {"message" : "이미 등록되어있는 메일 주소입니다."}
    crud.create_user(db=db,user=user)
    return {"message": user.email + "이 등록되었습니다."}


conf = ConnectionConfig(
    MAIL_USERNAME = os.getenv("User_mail"),
    MAIL_PASSWORD = os.getenv('User_password'),
    MAIL_FROM = os.getenv("User_mail"),
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_FROM_NAME="Desired Name",
    MAIL_TLS = True,
    MAIL_SSL = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

fm = FastMail(conf)

x = 10