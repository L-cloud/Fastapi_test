
import requests, os
from collections import defaultdict
from bs4 import BeautifulSoup
from typing import List, Dict
from celery import Celery
from celery.schedules import crontab
from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)
app = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost')

app.conf.timezone = 'UTC'



@app.task
def naver_journal(codes:List[str]) -> None : 
    url = "https://media.naver.com/journalist/015/" 
    db = SessionLocal()
    messages = {}
    for code in codes:
        req = requests.get(url + code)
        bs = BeautifulSoup(req.text,'html.parser')
        link = bs.find('a',{"class":"press_edit_news_link"})
        db_url = crud.get_Njournals_by_url(db, url=link['href'])
        if db_url:
            print("이미있음")
            continue
        journal = schemas.NjournalCreate(url = link['href'])    
        crud.create_Njournal(db=db,journal = journal)
        messages[link.find(class_ = "press_edit_news_title").text]= link['href']
    db.close()
    return messages
@app.task
def investing(codes:Dict[str,List[str]]) -> None:
    db = SessionLocal()
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}
    url =  "https://kr.investing.com/rates-bonds/"
    history = '-historical-data'
    messages = defaultdict(list)
    for key in codes:
        for n,c in codes[key]:
            req = requests.get(url + c + history,headers = headers)
            bs = BeautifulSoup(req.text, 'html.parser')
            body = bs.find('div',{"id" :"results_box"}).find('tbody').find('tr')
            date, rate = body.find('td').text, body.find('td',{"class":["greenFont","redFont"]}).text
            db_date = crud.get_DailyRate_by_date(db,date)
            if db_date:
                break  # 장 안 열어서 다른 상품도 x
            date = schemas.DailyRateCreate(date = date)   
            crud.create_DailyRate(db,date)
            messages[key].append(n + rate)
    db.close()
    return messages
@app.task
def send_mail(): # 여기서 메일 send를 하자
    print("시작")
    db = SessionLocal()
    users = [user.email for user in crud.get_users(db)]
    messages = []
    journal_args =["25212", "25162"]
    n = naver_journal.delay(journal_args)
    investing_args = {'미국':[["10년","u.s.-10-year-bond-yield"],["3년","u.s.-3-year-bond-yield"]],
                '그리스' : [["5년", "greece-5-year-bond-yield"],["10년", "greece-5-year-bond-yield"]],
                '독일':[['5년','germany-5-year-bond-yield'],['10년','germany-10-year-bond-yield']]} 
    v = investing.delay(investing_args)
    print(n,v)
    

app.conf.beat_schedule = {
    'send_mail':{
        'task' : 'tasks.send_mail',
        'schedule' : 15,
    }
}


# print(os.getenv("User_mail"))
# os.getenv('Uset_password')

# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_USE_TLS = True
# EMAIL_PORT = 587


# conf = ConnectionConfig(
#     MAIL_USERNAME = os.getenv("User_mail"),
#     MAIL_PASSWORD = os.getenv('Uset_password'),
#     MAIL_FROM = os.getenv("User_mail"),
#     MAIL_PORT = 587,
#     MAIL_SERVER = "smtp.gmail.com",
#     MAIL_FROM_NAME="Desired Name",
#     MAIL_TLS = True,
#     MAIL_SSL = False,
#     USE_CREDENTIALS = True,
#     VALIDATE_CERTS = True
# )

# html = """
# <p>Hi this test mail, thanks for using Fastapi-mail</p> 
# """

# async def simple_send():
#     message = MessageSchema(
#         subject="Fastapi-Mail module",
#         recipients=email.dict().get("email"),  # List of recipients, as many as you can pass 
#         body=html,
#         subtype="html"
#         )

#     fm = FastMail(conf)
#     await fm.send_message(message)

# 하나의 db가 더 필요한가..?