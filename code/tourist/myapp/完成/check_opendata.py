import csv
from os.path import join, dirname
from dotenv import load_dotenv, find_dotenv
import os
import requests
import re
import populartimes
import json
# response = requests.get("https://media.taiwan.net.tw/XMLReleaseALL_public/scenic_spot_C_f.json")
# data = response.content.decode("utf-8-sig")  # 使用 utf-8-sig 編碼解碼資料

# # 將文字轉換為 JSON 格式
# json_data = json.loads(data)

# for data in json_data['XML_Head']['Infos']['Info']:
#     if data['Region'] == "臺北市":
#         print(data['Town'])



# 取得基本資料json
def get_textsearch(GOOGLE_PLACES_API_KEY,address,a_type):
    URL = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
    response = requests.get(URL + "query=" + f'{address[0]}{address[1]}{a_type}' + '&language=zh-TW'+"&key=" + GOOGLE_PLACES_API_KEY)
    data = response.content.decode('unicode_escape')
    data = data.replace('"<a href=', '')
    data = re.sub(r'>.*</a>"', '', data)

    f = open(os.getcwd()+f'/{address[0]}{address[1]}{a_type}.json', 'a',encoding='utf-8')
    f.write(data)
    f.close()


with open('opendata.csv',newline='',encoding='utf-8')as csvfile:
    address_list = list(csv.reader(csvfile))
    list(address_list)
    for a_name in address_list:
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