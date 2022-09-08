from fastapi import FastAPI,Request,Depends,HTTPException
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import EmailStr,BaseModel
from typing import Union
from sqlalchemy.orm import Session
from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

class Data(BaseModel):
    email: EmailStr
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

@app.post("/")
async def main(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        return RedirectResponse(url = '/exist',status_code=302)
    crud.create_user(db=db,user=user)
    return RedirectResponse(url='/', status_code=302)


@app.get('/exist')
async def exist():
    return {'message' : "already exist"}
