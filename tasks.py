
import requests
from collections import defaultdict
from bs4 import BeautifulSoup
from typing import List, Dict
from celery import Celery
from celery.schedules import crontab
from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine
from celery.result import allow_join_result
from fastapi_mail import MessageSchema
from main import fm
from asgiref.sync import async_to_sync
models.Base.metadata.create_all(bind=engine)
app_celery = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost')

app_celery.conf.timezone = 'UTC'



@app_celery.task
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
            continue
        journal = schemas.NjournalCreate(url = link['href'])    
        crud.create_Njournal(db=db,journal = journal)
        messages[link.find(class_ = "press_edit_news_title").text]= link['href']
    db.close()
    return messages

@app_celery.task
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
            db_date = crud.get_DailyRate_by_date(db,key+n+date)
            if db_date:
                break  
            date = schemas.DailyRateCreate(date = key+n+date)   
            crud.create_DailyRate(db,date)
            messages[key].append(n + " " + rate)
    db.close()
    return messages

@app_celery.task()
def make_mail(): 
    db = SessionLocal()
    users = [user.email for user in crud.get_users(db)]
    messages = {}
    journal_args =["25212", "25162"]
    naver_scrapying = naver_journal.delay(journal_args)
    investing_args = {'미국 ':[["10년","u.s.-10-year-bond-yield"],["3년","u.s.-3-year-bond-yield"]],
                '그리스 ' : [["5년", "greece-5-year-bond-yield"],["10년", "greece-5-year-bond-yield"]],
                '독일 ':[['5년','germany-5-year-bond-yield'],['10년','germany-10-year-bond-yield']]} 
    investing_scraping = investing.delay(investing_args)
    with allow_join_result():
        messages.update(naver_scrapying.get())
        messages.update(investing_scraping.get())
        html = ''
        for key in messages:
            html += f'<p> {key}  {messages[key]} </p>'
        print(html)
        async_to_sync(send_mail)(html,users)
    return
async def send_mail(html:str,users:List[str]):
    
    mail = MessageSchema(
        subject="오늘의 변동",
        recipients=users,  # List of recipients, as many as you can pass 
        body=html,
        subtype="html"
        )
    
    await fm.send_message(mail)
    
    return

app_celery.conf.beat_schedule = {
    'send_mail':{
        'task' : 'tasks.make_mail',
        'schedule' : 15,
    }
}