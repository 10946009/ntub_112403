import csv
from os.path import join, dirname
from dotenv import load_dotenv, find_dotenv
import os
import requests
import re
import populartimes
import json

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path, override=True)  # 設定 override 才會更新變數
GOOGLE_PLACES_API_KEY = os.environ.get("GOOGLE_PLACES_API_KEY")

a_type_list = ['酒吧']

# 取得基本資料json
def get_textsearch(GOOGLE_PLACES_API_KEY,address,a_type):
    URL = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
    response = requests.get(URL + "query=" + f'{address[0]}{address[1]}{a_type}' + '&language=zh-TW'+"&key=" + GOOGLE_PLACES_API_KEY)
    data = response.content.decode('unicode_escape')
    data = data.replace('"<a href=', '')
    data = re.sub(r'>.*</a>"', '', data)

    f = open(os.getcwd()+f'/{address[0]}{address[1]}{a_type}.json', 'w',encoding='utf-8')
    f.write(data)
    f.close()

# 取得擁擠資料json，放入key和景點id
def get_populartimes(datafile,GOOGLE_PLACES_API_KEY,a_type):
    result = []
    
    with open(datafile, encoding='utf-8') as file:
        data = json.load(file)
        for num in range(len(data['results'])):
            times = 0
            placeid = data['results'][num]['place_id'] 
            try:
                p = populartimes.get_id(GOOGLE_PLACES_API_KEY,placeid)
                times+=1
                print(placeid,times)
            except:
                while 1:
                    
                    p = populartimes.get_id(GOOGLE_PLACES_API_KEY,placeid)
                    times+=1
                    print(placeid,'生成失敗...',times)
                    break
            result.append(p)
    # 修改以下的寫入方式，增加 ensure_ascii 和 indent 參數
    with open(os.getcwd() + f'/{address[0]}{address[1]}{a_type}擁擠資訊.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

def get_details(datafile,GOOGLE_PLACES_API_KEY,a_type):
    result = []
    with open(datafile, encoding='utf-8') as file:
        data = json.load(file)
        for num in range(len(data['results'])):
            placeid = data['results'][num]['place_id']
            url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={placeid}&language=zh-TW&key={GOOGLE_PLACES_API_KEY}"
            response = requests.get(url)
            opendata = response.json()
            result.append(opendata)
    with open(os.getcwd() + f'/{address[0]}{address[1]}{a_type}營業時間.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

# 將所有市區路的資料取得
with open('臺北市bar.csv',newline='',encoding='utf-8')as csvfile:
    address_list = list(csv.reader(csvfile))[1:]
    list(address_list)
    # address= ['市區','路']
    #1-10
    address_list = [[x[0],""] for x in address_list]
    print(address_list)
    for address in address_list:
        print(address[0],address[1])
        
        for a_type in a_type_list:
            if f'{address[0]}{address[1]}{a_type}.json' in os.listdir():
                print(f'{address[0]}{address[1]}{a_type}.json','已存在')
            else:
                print('產生',f'{address[0]}{address[1]}{a_type}.json')
                get_textsearch(GOOGLE_PLACES_API_KEY,address,a_type)

            filename = f'{os.getcwd()}/{address[0]}{address[1]}{a_type}.json'

            if f'{address[0]}{address[1]}{a_type}擁擠資訊.json' in os.listdir():
                print(f'{address[0]}{address[1]}{a_type}擁擠資訊.json','已存在')
            else: 
                print('產生',f'{address[0]}{address[1]}{a_type}擁擠資訊.json')
                get_populartimes(filename,GOOGLE_PLACES_API_KEY,a_type)

            if f'{address[0]}{address[1]}{a_type}營業時間.json' in os.listdir():
                print(f'{address[0]}{address[1]}{a_type}營業時間.json','已存在')
            else: 
                print('產生',f'{address[0]}{address[1]}{a_type}營業時間.json')
                get_details(filename,GOOGLE_PLACES_API_KEY,a_type) 