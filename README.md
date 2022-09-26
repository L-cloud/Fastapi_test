# FastAPI
매일 금리 변동을 스크래핑 해서 메일로 보내주는 사이트

### 시스템 구조

https가 아닌 http로 통신 하였습니다.

![](https://miro.medium.com/proxy/0*UYL0WslDwLEF6qoY)
![](https://user-images.githubusercontent.com/14961526/154876820-52182eab-4295-42e5-960c-19ede6d5fff5.png)

>webserver는 NGINX를 사용했습니다. <br>
celery의 broker, backend는 redis를 사용했습니다.<br>
db는 sqlite3를 사용했습니다.


## 구현기능
* celery 매일 5시 30분 마다 특정 사이트 스크래핑 및 Email 전송
* Email 등록

## Tools

* FastAPI
* python3
* celery
* Nginx
* Javascript

# 동작화면

메인 페이지 입니다. 
![](https://postfiles.pstatic.net/MjAyMjA5MjZfOTAg/MDAxNjY0MTU1MjU3MjY4.m5-4Qz5vxKlvfUT57_Vgm-GW9iheQA-y04M0ObFp0yYg.-PRD6RPj_6PWqJCQTgVStZ32AsyCaBS475xcD1j6n2wg.PNG.supporterleo/image.png?type=w966)

올바른 Email 주소가 들어왔을 경우 아래와 같이 이모티콘이 변합니다.
![](https://postfiles.pstatic.net/MjAyMjA5MjZfMjk3/MDAxNjY0MTU1MzQzNTcz.oDvA-QfRjf6g7k3Y6uC0nMjzLd4zzDg52rnkQKOQakwg.oAcCJFcdFCJFOQjtVgBWZ3IeGfg1BpfeJh-IAVH7xJYg.PNG.supporterleo/image.png?type=w966)


## 스크래핑하는 사이트

https://kr.investing.com/rates-bonds/
https://media.naver.com/journalists/015