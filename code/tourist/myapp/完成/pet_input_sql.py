import psycopg2
import os
import csv
import json
from sqltool import Postgres
tool = Postgres()
types_list = []

a_type_list = ['寵物友善公園']

att_types = {
    'tourist_attraction':1, #旅遊景點
    'point_of_interest':2, #興趣點
    'establishment':3, #機構
    'park':4, #公園
    'place_of_worship':5, #宗教場所
    'food':6, #食物
    'museum':7, #博物館
    'landmark':8, #地標;標誌性建築
    'grocery_or_supermarket':9, #雜貨店或超市
    'store':10, #商店
    'restaurant':11, #餐廳
    'library':12, #圖書館
    'school':13, #學校
    'jewelry_store':14, #珠寶店
    'church':15, #教堂(X)
    'cafe':16, #咖啡廳
    'mosque':17, #清真寺(宗教類)
    'bakery':18, #麵包店
    'home_goods_store':19, #家居商品商店
    'art_gallery':20, #藝術
    'night_view':21, #夜景
    'hindu_temple':22, #印度教寺廟
    'pet_store':23, #寵物店
    'movie_theater':24, #電影院
    'amusement_park':25, #遊樂園
    'zoo':26, #動物園
    'meal_delivery':27, #外送
    'aquarium':28, #水族館
    'flower':29, #花
    'natural_feature':30, #自然特徵
    'night_market':31, #夜市
    'stadium':32,#體育
    'campground':33, #露營地
    'shopping_mall':34, #購物商場
    'electronics_store':35, #電子商店
    'spa':36, #溫泉
    'DIY':37, #DIY
    'bar':100,
    'liquor_store':101,
    'night_club':102,
    'furniture_store':103,
    'storage':104,
    'bicycle_store':105,
    'meal_takeaway':106,
    'hospital':201,
    'health':202,
    'department_store':203,
    'lodging':204,
    'book_store':205,
    'beauty_salon':206,
}
# data=

# 資料庫
def input_address(tool,data, data_crowd, data_opening_phone, num,att_types,att_type_file):
    place_id = data["results"][num]["place_id"]
    try:
        photo_check = data["results"][num]["photos"][0]["photo_reference"]  # 改變第一個num
        photo = photo_check if photo_check is not None else ""
    except:
        photo = ""
    a_name = data_opening_phone[num]["result"]["name"]
    check_unique = tool.read(
        f"SELECT * FROM myapp_pet WHERE place_id ILIKE '{place_id}';"
    )
    print(check_unique)
    if len(check_unique) != 0:
        return
    address = data_opening_phone[num]["result"]["formatted_address"]
    location_x = data["results"][num]["geometry"]["location"]["lat"]
    location_y = data["results"][num]["geometry"]["location"]["lng"]
    print(address)
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
        rating = data["results"][num]["rating"]
    except:
        rating = 0
    try:
        rating_total = data["results"][num]["user_ratings_total"]
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
    for a_t in data["results"][num]["types"]:
        att_type.append(att_types[a_t])

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
        "stay_time",
        "hot_month",
        "a_type",
        "hit",
        "detail"
    ]
    print(input_column)
    s_len = ("%s," * len(input_column))[:-1]
    sql = f"INSERT INTO myapp_pet ({','.join(input_column)}) VALUES ({s_len})"
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
                stay_time,
                hot_month,
                att_type,
                0,
                att_type_file
            )
        ],
    )

    input_crowd_opening(tool,data, data_crowd, data_opening_phone, num)

# 確認有甚麼標籤
def check_new_att_type(data,num,types_list):
    types = data["results"][num]["types"]
    
    for t in types:
        if t not in types_list:
            types_list.append(t)
    return types_list

# DATA可以抓placeid
def input_crowd_opening(tool,data, data_crowd, data_opening_phone, num):
    tool = Postgres()
    place_id = data["results"][num]["place_id"]
    # # 擁擠populartimes
    # # 營業時間 weekday_text
    sql1 = f"SELECT * FROM myapp_pet WHERE place_id = '{place_id}';"
    a_id = tool.read(sql1)[0][0]

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
            "p_id",
        ]
        print( week,
                     crowd,
                     opening,
                     a_id,)
        week+=1
        s_len = ("%s," * len(input_column))[:-1]
        sql = f"INSERT INTO myapp_pet_crowd_opening ({','.join(input_column)}) VALUES ({s_len})"
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


# check_list=[]
# with open("需刪除的id.csv", newline="", encoding="utf-8") as csvfile_check:
#     check_list = list(csv.reader(csvfile_check))
#     check_list = [x[0] for x in check_list]
# 把json資料都抓出來 然後使用函數

with open("臺北市bar.csv", newline="", encoding="utf-8") as csvfile:
    address_list = list(csv.reader(csvfile))
    list(address_list)
    address_list = [[x[0],""] for x in address_list]
    for address in address_list[1:]:
        print(address[0],address[1])
        for att_type_file in a_type_list :
            with open(f"{address[0]}{address[1]}{att_type_file}.json", encoding="utf-8") as file:
                data = json.load(file)

            with open(f"{address[0]}{address[1]}{att_type_file}擁擠資訊.json", encoding="utf-8") as file:
                data_crowd = json.load(file)

            with open(f"{address[0]}{address[1]}{att_type_file}營業時間.json", encoding="utf-8") as file:
                data_opening_phone = json.load(file)
                for num in range(len(data["results"])):
                    input_address(tool,data, data_crowd, data_opening_phone, num,att_types,att_type_file)
                    types_list = check_new_att_type(data,num,types_list)
                    


        # except :
        #         print(f"{address[0]}{address[1]} error")
        #         continue
