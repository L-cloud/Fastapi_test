import requests,time
from bs4 import BeautifulSoup
from typing import List, Dict
class Naver_Journal:
    '''
    get_url 함수 safe 하게 처리
    DB 연동해서 없을 때만 추가, message 추가 될 때만 message return
    '''
    url = "https://media.naver.com/journalist/015/" 
    def __init__(self,code:str) -> None:
        self.code = code
    def get_url_headline(self) -> List[str]: 
        # 여기 get에 대한 오류도 해야함
        start = time.time()
        req = requests.get(self.url + self.code)
        bs = BeautifulSoup(req.text,'html.parser')
        a = bs.find('a',{"class":"press_edit_news_link"})
        print(f'{time.time()-start:.3f}ms') # 응답 속도 비교
        return [a.find(class_ = "press_edit_news_title").text, a['href']]

class Investing:
    '''
    get_interest_rage 함수 safe 하게 처리 되어야함
    DB 연동해서 없을 때만 추가하고, message 추가 될 때만 message return 아니면 None 
    '''
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}
    url =  "https://kr.investing.com/rates-bonds/"
    def __init__(self,code:List[str],country:str) -> None:
        self.code = code
        self.country = country # Message 에 들어갈 녀석
    def get_interest_rage(self) -> Dict[str,Dict[str,List]]:
        message = [[self.country]]
        start = time.time()
        for n,c in self.code:
            req = requests.get(self.url + c,headers = self.headers)
            bs = BeautifulSoup(req.text, 'html.parser')
            m = bs.find('div',{"class" :"top bold inlineblock"}).text.split() 
            message.append([n] + m) # 3개월 ['3.195', '+0.004', '+0.13%']
        print(f'{time.time()-start:.3f}ms')# 응답 속도 비교
        return message

naver= ["25212", "25162"]
investing = {'미국':[["10년 물","u.s.-10-year-bond-yield"],["3년 물","u.s.-3-year-bond-yield"]],
'그리스' : [["5년 물", "greece-5-year-bond-yield"],["10년 물", "greece-5-year-bond-yield"]],
'독일':[['5년 물','germany-5-year-bond-yield'],['10년 물','germany-10-year-bond-yield']]}

for i in naver:
    print(Naver_Journal(i).get_url_headline())
for i in investing:
    print(Investing(investing[i],i).get_interest_rage())