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
# def get_textsearch(GOOGLE_PLACES_API_KEY,a_name):
#     URL = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?"
#     response = requests.get(URL + "input=" + "臺北市" +a_name + "&inputtype=textquery&fields=place_id%2Cformatted_address%2Cname%2Crating%2Copening_hours%2Cgeometry%2Cuser_ratings_total%2Cphoto%2Ctype" +"&key=" + GOOGLE_PLACES_API_KEY)
#     # response = requests.get(URL + "input=" + a_name + '&language=zh-TW'+"&key=" + GOOGLE_PLACES_API_KEY)
#     data = response.content.decode('unicode_escape')
#     data = data.replace('"<a href=', '')
#     data = re.sub(r'>.*</a>"', '', data)
#     return data

# 將景點資料寫入json檔
# with open('opendata.csv',newline='',encoding='utf-8')as csvfile:
#     address_list = list(csv.reader(csvfile))
#     # list(address_list)
#     result = []
#     try:
#         for a_name in address_list:
#             data = get_textsearch(GOOGLE_PLACES_API_KEY,a_name[0])
#             json_data = json.loads(data)
#             print(a_name[0],",新增的：",json_data['candidates'][0]["name"])
#             result.append(json_data)
#     except:
#         print(a_name[0],"沒抓到")
#         # print("這QQQ",data)
#     # print("我在這",result)
#     f = open(os.getcwd()+f'/opendata.json', 'w',encoding='utf-8')
#     f.write(json.dumps(result))
#     f.close()
# 還沒寫好
        # filename = f'{os.getcwd()}/{address[0]}{address[1]}{a_type}.json'
        # get_populartimes(filename,GOOGLE_PLACES_API_KEY,a_type)
        # get_details(filename,GOOGLE_PLACES_API_KEY,a_type)