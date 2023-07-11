import csv
from os.path import join, dirname
from dotenv import load_dotenv, find_dotenv
import os
import requests
import re
import populartimes
import json

from sqltool import Postgres
tool = Postgres()

# 抓opendata的資料
# response = requests.get("https://media.taiwan.net.tw/XMLReleaseALL_public/scenic_spot_C_f.json")
# data = response.content.decode("utf-8-sig")  # 使用 utf-8-sig 編碼解碼資料

# # 將文字轉換為 JSON 格式
# json_data = json.loads(data)

# for data in json_data['XML_Head']['Infos']['Info']:
#     if data['Region'] == "臺北市":
#         print(data['Town'])


# dotenv_path = join(dirname(__file__), ".env")
# load_dotenv(dotenv_path, override=True)  # 設定 override 才會更新變數
# GOOGLE_PLACES_API_KEY = os.environ.get("GOOGLE_PLACES_API_KEY")


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


# 抓擁擠資訊
# def get_populartimes(datas,GOOGLE_PLACES_API_KEY,check_list):
#     result = []
    
#     for data in datas:
#         times = 0
#         place_id = data["candidates"][0]["place_id"]
#         if place_id not in check_list:
#             continue
#         try:
#             p = populartimes.get_id(GOOGLE_PLACES_API_KEY,place_id)
#             times+=1
#             print(place_id,times)
#         except:
#             while 1:
#                 p = populartimes.get_id(GOOGLE_PLACES_API_KEY,place_id)
#                 times+=1
#                 print(place_id,'生成失敗...',times)
#                 break
#         result.append(p)
    
#     f = open(os.getcwd()+f'/opendata擁擠資訊.json', 'w',encoding='utf-8')
#     f.write(json.dumps(result))
#     f.close()

# 抓營業時間
# def get_details(datas,GOOGLE_PLACES_API_KEY,check_list):
#     result = []
#     for data in datas:
#         place_id = data["candidates"][0]["place_id"]
#         if place_id not in check_list:
#             continue
#         url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&language=zh-TW&key={GOOGLE_PLACES_API_KEY}"
#         response = requests.get(url)
#         opendata = response.json()
#         result.append(opendata)
 
#     f = open(os.getcwd()+f'/opendata營業時間.json', 'w',encoding='utf-8')
#     f.write(json.dumps(result))
#     f.close()


types_list = []

att_types = {
    'tourist_attraction':1,
    'point_of_interest':2,
    'establishment':3,
    'park':4,
    'place_of_worship':5,
    'food':6,
    'museum':7,
    'landmark':8,
    'grocery_or_supermarket':9,
    'store':10,
    'restaurant':11,
    'library':12,
    'school':13,
    'jewelry_store':14,
    'church':15,
    'cafe':16,
    'mosque':17,
    'bakery':18,
    'home_goods_store':19,
    'art_gallery':20,
    'route':21,
    'hindu_temple':22,
    'pet_store':23,
    'movie_theater':24,
    'amusement_park':25,
    'zoo':26,
    'meal_delivery':27,
    'aquarium':28,
    'liquor_store':29, #臺灣菸酒公司 士林營業所
    'natural_feature':30, #大崙頭山、彩虹碼頭、陽明山
    'premise':31, #台北公會堂、臺北圓環、世貿公園
    'stadium':32,#臺北小巨蛋
    'campground':33, #碧山露營場
    'shopping_mall':34, #三創生活園區
    'electronics_store':35, #三創生活園區

}
# 景點資料庫
def input_address(tool,data, data_crowd, data_opening_phone,att_types,check_id_list):
    place_id = data["candidates"][0]["place_id"]
    if place_id not in check_id_list:
        return
    num = check_id_list.index(place_id)
    try:
        photo_check = data["candidates"][0]["photos"][0]["photo_reference"]  # 改變第一個num
        photo = photo_check if photo_check is not None else ""
    except:
        photo = ""
    a_name = data["candidates"][0]["name"]
    check_unique = tool.read(
        f"SELECT * FROM myapp_attractions WHERE place_id ILIKE '{place_id}';"
    )
    if len(check_unique) != 0:
        return
    address = data["candidates"][0]["formatted_address"]
    location_x = data["candidates"][0]["geometry"]["location"]["lat"]
    location_y = data["candidates"][0]["geometry"]["location"]["lng"]
    try:
        formatted_phone = data_opening_phone[num]["result"].get(
            "formatted_phone_number"
        )
        phone = formatted_phone if formatted_phone is not None else ""
    except:
        phone = ""
    # tags = data['results'][num]['types']
    try:
        opening = data_opening_phone[num]["result"]["opening_hours"]["weekday_text"]
    except:
        opening = "{}"

    try:
        rating = data["candidates"][0]["rating"]
    except:
        rating = 0
    try:
        rating_total = data["candidates"][0]["user_ratings_total"]
    except:
        rating_total = 0
    
    score = 0
    try:
        stay_time = sum(data_crowd[num]["time_spent"]) // len(
            data_crowd[num]["time_spent"]
        )
    except:
        stay_time = 0
    hot_month = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    att_type = []
    for a_t in data["candidates"][0]["types"]:
        try:
            att_type.append(att_types[a_t])
        except:
            print(a_t)
            continue

    # 放入資料庫
    input_column = [
        "place_id",
        "photo",
        "a_name",
        "address",
        "location_x",
        "location_y",
        "phone",
        "rating",
        "rating_total",
        "score",
        "stay_time",
        "hot_month",
        "att_type",
    ]
    s_len = ("%s," * len(input_column))[:-1]
    sql = f"INSERT INTO myapp_attractions ({','.join(input_column)}) VALUES ({s_len})"
    print(a_name, "放入資料庫")
    tool.create_multi(
        sql,
        [
            (
                place_id,
                photo,
                a_name,
                address,
                location_x,
                location_y,
                phone,
                rating,
                rating_total,
                score,
                stay_time,
                hot_month,
                att_type,
            )
        ],
    )
    input_crowd_opening(tool,place_id,data, data_crowd, data_opening_phone, num)

# DATA可以抓placeid
def input_crowd_opening(tool,place_id,data, data_crowd, data_opening_phone, num):
    print(num)
    tool = Postgres()
    # 擁擠populartimes
    # 營業時間 weekday_text
    sql1 = f"SELECT * FROM myapp_attractions WHERE place_id = '{place_id}';"
    a_id = tool.read(sql1)[0][0]
    print(data_crowd[num]["name"])
    for week in range(7):
        try:
            crowd = data_crowd[num]['populartimes'][week]['data']
        except:
            crowd = []
        try:
            opening = list(data_opening_phone[num]['result']['current_opening_hours']['weekday_text'][week][5:].split(','))
            if len(data_opening_phone[num]['result']['current_opening_hours']['weekday_text']) != 7:
                print('有人沒七筆!')
        except:
            opening = []
        

 
        #放入資料庫
        input_column = [
            "week",
            "crowd",
            "opening",
            "a_id",
        ]
        week+=1
        s_len = ("%s," * len(input_column))[:-1]
        sql = f"INSERT INTO myapp_crowd_opening ({','.join(input_column)}) VALUES ({s_len})"
        tool.create_multi(
            sql,
            [
                (
                    week,
                    crowd,
                    opening,
                    a_id,
                )
            ],
        )
        print("a_id",a_id, "新增擁擠資訊")

# 確認有甚麼標籤
def check_new_att_type(data,num,types_list):
    types = data["candidates"][0]["types"]
    
    for t in types:
        if t not in types_list:
            types_list.append(t)
    return types_list

# 已整理的ID
with open("opendata對照表.csv", newline="", encoding="utf-8") as csvfile_check_id:
    check_id_list = list(csv.reader(csvfile_check_id))
    check_id_list = [x[0] for x in check_id_list]

# 未整理
with open("需刪除的景點id.csv", newline="", encoding="utf-8") as csvfile_check:
    check_list = list(csv.reader(csvfile_check))
    check_list = [x[0] for x in check_list]

with open("opendata.json", encoding="utf-8") as file:
        datas = json.load(file)

        # get_details(datas,GOOGLE_PLACES_API_KEY,check_list) #抓營業時間
        # get_populartimes(datas,GOOGLE_PLACES_API_KEY,check_list) #抓取擁擠資訊

with open(f"opendata擁擠資訊.json", encoding="utf-8") as file:
        data_crowd = json.load(file)
with open(f"opendata營業時間.json", encoding="utf-8") as file:
        data_opening_phone = json.load(file)
        # 放入資料庫
        for data in datas:
            input_address(tool,data, data_crowd, data_opening_phone,att_types,check_id_list)