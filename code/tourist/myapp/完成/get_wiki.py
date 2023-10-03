import requests
from bs4 import BeautifulSoup
import psycopg2
import os
import csv
import json
from sqltool import Postgres
import time
import re
tool = Postgres()
TIMESLEEP = 1
HEARDERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}
def get_crowd(url):
    html = requests.get(url,headers=HEARDERS)
    html.encoding = 'UTF-8'
    htmltext = BeautifulSoup(html.text, 'html.parser')
    return htmltext

def wiki_detail(url):
    print(url)
    try:
        htmltext = get_crowd(url)
        detail = htmltext.find('p')
        if '座標：'in detail.get_text() :
            return ''
    except:
        return ''
    
    detail_text = re.sub(r'\[\d+\]', '', detail.get_text())
    detail_text = detail_text.replace('\n','')
    return detail_text
    

wiki = "https://zh.wikipedia.org/zh-tw/"

all_attractions_name = tool.read("SELECT a_name FROM myapp_attractions;")
all_attractions_name = [x[0] for x in all_attractions_name]

for attractions in all_attractions_name:
    
    wek = wiki_detail(wiki+attractions)
    print([wek])
    if wek == '':
        continue
    data = tool.read(
        f"SELECT * FROM myapp_attractions WHERE a_name ILIKE '{attractions}';"
    )
    sql =f"UPDATE myapp_attractions SET detail = %s WHERE a_name = %s;"
    tool.update(sql,(wek,attractions))
    time.sleep(TIMESLEEP)