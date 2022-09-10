
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
        print(db_url.url)
        if db_url:
            print("이미 저장됨")
            continue
        journal = schemas.NjournalCreate(url = link['href'])    
        crud.create_Njournal(db=db,journal = journal)
        tempt_value.append([link.find(class_ = "press_edit_news_title").text, link['href']])
    db.close()
    return tempt_value

@app.task
def investing1(codes:Dict[str,List[str]]) -> None:
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}
    url =  "https://kr.investing.com/rates-bonds/"
    tempt = defaultdict(list)
    # 주말 데이터 확인하고 db 뭐 저장할지 정해야함
    print("codes = ",codes)
    for key in codes:
        for n,c in codes[key]:
            req = requests.get(url + c,headers = headers)
            bs = BeautifulSoup(req.text, 'html.parser')
            m = bs.find('div',{"class" :"top bold inlineblock"}).text.split() 
            tempt[key].append([n] + m)
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
        'schedule':crontab(hour=5, minute=0),      
        'args': {'미국':[["10년 물","u.s.-10-year-bond-yield"],["3년 물","u.s.-3-year-bond-yield"]],
                '그리스' : [["5년 물", "greece-5-year-bond-yield"],["10년 물", "greece-5-year-bond-yield"]],
                '독일':[['5년 물','germany-5-year-bond-yield'],['10년 물','germany-10-year-bond-yield']]}   
    }    
}