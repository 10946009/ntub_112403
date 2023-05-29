import json
import os
import populartimes
from os.path import join, dirname
from dotenv import load_dotenv, find_dotenv
import requests
import googlemaps


dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path, override=True)  # 設定 override 才會更新變數哦！
GOOGLE_PLACES_API_KEY = os.environ.get("GOOGLE_PLACES_API_KEY")




# 抓取每個資料欄位的資料
with open(f'{os.getcwd()}/臺北市松山區三民路.json', encoding='utf-8') as file:
    data = json.load(file)
place = data['results'][0]['place_id']
photo = data['results'][0]['photos'][0]['photo_reference']  #改變第一個0
a_name = data['results'][0]['name']
address = data['results'][0]['formatted_address']
location_x = data['results'][0]['geometry']['location']['lat']
location_y = data['results'][0]['geometry']['location']['lng']
tags = data['results'][0]['types']
rating = data['results'][0]['rating']
score = 0
Comment = []
# # -----------------抓取crowd、stay_time欄位
# p = populartimes.get_id(GOOGLE_PLACES_API_KEY, place)  #(key,place_id)
# crowd = p['populartimes']  #欄位
# try:
#     stay_time = sum(p['time_spent']) // len(p['time_spent'])  #欄位
# except:
#     stay_time = []  #欄位
# # --------------------------------------------------------------------------

# # -----------------抓取opening、phone欄位
# url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place}&fields=name,formatted_address,opening_hours&key={GOOGLE_PLACES_API_KEY}"
# # 發送 API 請求並取得回應
# response = requests.get(url)
# open = response.json()
# opening = open['result']['opening_hours']['weekday_text']  # 欄位

# # 解析API響應獲取電話號碼
# if open["status"] == "OK":
#     result = open["result"]
#     phone_number = result.get("formatted_phone_number")
#     if phone_number:
#        phone = phone_number  #欄位
#     else:
#        phone = "未找到電話號碼"  #欄位
# else:
#     print("請求失敗:", open["status"])
# # --------------------------
# # 範例
# open = {'html_attributions': [], 'result': {'formatted_address': 'Fuyuan St, Songshan District, Taipei City, Taiwan 105', 'name': 'Sanmin Park', 'opening_hours': {'open_now': True, 'periods': [{'open': {'day': 0, 'time': '0000'}}], 'weekday_text': ['Monday: Open 24 hours', 'Tuesday: Open 24 hours', 'Wednesday: Open 24 hours', 'Thursday: Open 24 hours', 'Friday: Open 24 hours', 'Saturday: Open 24 hours', 'Sunday: Open 24 hours']}}, 'status': 'OK'}
# print(open)
# # -------------------------
# # 列印商家資訊和營業時間
# hours = data["result"]["opening_hours"]["weekday_text"]
# print(f"商家名稱：{name}")
# print(f"商家地址：{address}")
# print("營業時間：")
# for hour in hours:
#     print(hour)
# # --------------------------------------------------------------------------


## -----------------------------------抓圖片用-------------------------------------
# import requests

# photo_reference = "your_photo_reference"  # 替换为您的实际photo_reference值
# max_width = 500  # 设置所需的最大宽度
# max_height = 500  # 设置所需的最大高度

## 构建请求URL，包括maxwidth和maxheight参数
# url = f"https://maps.googleapis.com/maps/api/place/photo?photoreference={photo_reference}&maxwidth={max_width}&maxheight={max_height}&key=your_api_key"
## 将your_api_key替换为您的实际API密钥

## 发送HTTP请求获取照片
# response = requests.get(url)

## 将照片保存到文件
# with open("photo.jpg", "wb") as file:
#     file.write(response.content)
## --------------------------------------------------------------------------


# 寫成整理後資料
# with open('臺北市松山區三民路.json', 'r',encoding='utf-8') as file:
#     content = file.read()
    

# with open('臺北市松山區三民路_整理後2.json', 'w',encoding='utf-8') as f:
#     f.write(content)
