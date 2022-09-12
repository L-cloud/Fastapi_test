
import requests
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
    for code in codes:
        tempt_value = []
        req = requests.get(url + code)
        bs = BeautifulSoup(req.text,'html.parser')
        link = bs.find('a',{"class":"press_edit_news_link"})
        db_url = crud.get_Njournals_by_url(db, url=link['href'])
        if db_url:
            continue
        journal = schemas.NjournalCreate(url = link['href'])    
        crud.create_Njournal(db=db,journal = journal)
        tempt_value.append([link.find(class_ = "press_edit_news_title").text, link['href']])
    db.close()
    return tempt_value

@app.task
def investing(codes:Dict[str,List[str]]) -> None:
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}
    url =  "https://kr.investing.com/rates-bonds/"
    history = '-historical-data'
    tempt = defaultdict(list)
    db = SessionLocal()
    for key in codes:
        for n,c in codes[key]:
            req = requests.get(url + c + history,headers = headers)
            bs = BeautifulSoup(req.text, 'html.parser')
            body = bs.find('div',{"id" :"results_box"}).find('tbody').find('tr')
            date, rate = key+ n + body.find('td').text, body.find('td',{"class":{"greenFront","redFont"}}).text
            db_date = crud.get_DailyRate_by_date(db,date)
            if db_date:
                break  # 장 안 열어서 다른 상품도 x
            date = schemas.DailyRateCreate(date = date)   
            crud.create_DailyRate(db,date)
            tempt[key].append(rate)
    db.close()
    return tempt

app.conf.beat_schedule = {
    'naver_journal': {  
        'task': 'tasks.naver_journal',  
        'schedule':15,
        # 'schedule':crontab(hour=5, minute=0),        
        'args': [["25212", "25162"]],  
    },
    'investing' : {
        'task': 'tasks.investing',  
        # 'schedule':crontab(hour=5, minute=0),      
        'schedule' : 15,
        'args': [{'미국':[["10년","u.s.-10-year-bond-yield"],["3년","u.s.-3-year-bond-yield"]],
                '그리스' : [["5년", "greece-5-year-bond-yield"],["10년", "greece-5-year-bond-yield"]],
                '독일':[['5년','germany-5-year-bond-yield'],['10년','germany-10-year-bond-yield']]}]   
    }    
}