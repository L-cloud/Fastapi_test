
import requests
from collections import defaultdict
from bs4 import BeautifulSoup
from typing import List, Dict
from celery import Celery
from celery.schedules import crontab

app = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost')

app.conf.timezone = 'UTC'
@app.task
def add(x, y):
    z = x + y
    print(z)
    return 3

@app.task
def naver_journal(codes:List[str]) -> None : 
    url = "https://media.naver.com/journalist/015/" 
    tempt_value = []
    for code in codes:
        req = requests.get(url + code)
        bs = BeautifulSoup(req.text,'html.parser')
        a = bs.find('a',{"class":"press_edit_news_link"})
        tempt_value.append([a.find(class_ = "press_edit_news_title").text, a['href']])
    return tempt_value

@app.task
def investing1(codes:Dict[str,List[str]]) -> None:
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}
    url =  "https://kr.investing.com/rates-bonds/"
    tempt = defaultdict(list)
    for key in codes:
        for n,c in codes[key]:
            req = requests.get(url + c,headers = headers)
            bs = BeautifulSoup(req.text, 'html.parser')
            m = bs.find('div',{"class" :"top bold inlineblock"}).text.split() 
            tempt[key].append([n] + m)
    return tempt

naver= ["25212", "25162"]
investing = {'미국':[["10년 물","u.s.-10-year-bond-yield"],["3년 물","u.s.-3-year-bond-yield"]],
'그리스' : [["5년 물", "greece-5-year-bond-yield"],["10년 물", "greece-5-year-bond-yield"]],
'독일':[['5년 물','germany-5-year-bond-yield'],['10년 물','germany-10-year-bond-yield']]}

app.conf.beat_schedule = {
    'naver_journal': {  
        'task': 'tasks.naver_journal',  
        'schedule':crontab(hour=5, minute=0),      
        'args': ["25212", "25162"]    
    },
    'investing' : {
        'task': 'tasks.investing',  
        'schedule':crontab(hour=5, minute=0),      
        'args': {'미국':[["10년 물","u.s.-10-year-bond-yield"],["3년 물","u.s.-3-year-bond-yield"]],
                '그리스' : [["5년 물", "greece-5-year-bond-yield"],["10년 물", "greece-5-year-bond-yield"]],
                '독일':[['5년 물','germany-5-year-bond-yield'],['10년 물','germany-10-year-bond-yield']]}   
    }    
}