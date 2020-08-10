import requests

from bs4 import BeautifulSoup
from datetime import datetime
 
# day_month = datetime.today().month    
# day_day = datetime.today().day        
 
# data = []
# url='https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query=%EC%BD%94%EB%A1%9C%EB%82%98+%ED%98%84%ED%99%A9' 
# hdr = {'Accept-Language': 'ko_KR,en;q=0.8', 'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36')}
# req = requests.get(url, headers=hdr)
# html = req.text
# soup = BeautifulSoup(html, 'html.parser')
# for i in soup.select('div[class=state_graph]'):
#     data.append(i.text)
# datasets = data[0]
# datasets = datasets.split("    ",10)
# datasets = datasets[1:]
# datasets = datasets[:-1]
# for i in range(0,4):
#     datasets[i] = datasets[i].replace(" ","")
    
# datasets.append(day_month)
# datasets.append(day_day)
# print(datasets)
# patient = datasets[0]
# dead = datasets[3]
# dayday = datasets[5]
# month = datasets[4]
 
 

url1 = "https://maker.ifttt.com/trigger/new_car_arrived/with/key/dQ2HNeN_GmArjr6OAkLru6"
r = requests.post(url1, data={"value1": "20년식", "value2":"1,200", "value3": "2600만원"})
 
