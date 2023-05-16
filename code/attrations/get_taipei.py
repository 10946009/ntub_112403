import csv
from os.path import join, dirname
from dotenv import load_dotenv, find_dotenv
import os
import requests
import re

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path, override=True)  # 設定 override 才會更新變數哦！
GOOGLE_PLACES_API_KEY = os.environ.get("GOOGLE_PLACES_API_KEY")
print(GOOGLE_PLACES_API_KEY)
URL = "https://maps.googleapis.com/maps/api/place/textsearch/json?"

# 之後要用迴圈把資料抓起來(範例:"新北市中和區景平路"+"景點")



with open('臺北市區路段資料.csv',newline='',encoding='utf-8')as csvfile:
    sp = list(csv.reader(csvfile))[1:]
    list(sp)
    for i in sp:
        r = requests.get(URL + "query=" + f'{i[0]}{i[1]}景點' + '&language=zh-TW'+"&key=" + GOOGLE_PLACES_API_KEY)
        data = r.content.decode('unicode_escape')
        data = data.replace('"<a href=', '')
        data = re.sub(r'>.*</a>"', '', data)
        f = open(os.getcwd()+f'/{i[0]}{i[1]}.json', 'w',encoding='utf-8')
        f.write(data)
        break
