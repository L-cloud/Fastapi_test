from fastapi import FastAPI,Request
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import EmailStr,BaseModel
from typing import Union

class Data(BaseModel):
    email: EmailStr

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static") 

@app.get("/", response_class=HTMLResponse)
async def main(request: Request,message:Union[None, str] = None):
    return templates.TemplateResponse('main.html',{"request" : request,"message" :message})

@app.post("/")
async def main2(email: Data):
    # email db check 후
    # 중복된에 따른 다른 return
    return RedirectResponse(url='/', status_code=302)

