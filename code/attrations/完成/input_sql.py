import psycopg2
import os
import csv
import json
from sqltool import Postgres


def input_address(data,data_crowd,data_opening_phone,num):
    tool = Postgres()
    place = data['results'][num]['place_id']
    try:
        photo_check = data['results'][num]['photos'][0]['photo_reference']  #改變第一個num
        photo = photo_check if photo_check is not None else ""
    except:
        photo = ""
    # print(photo)
    a_name = data['results'][num]['name']
    check_unique = tool.read(f"SELECT * FROM myapp_attractions WHERE place ILIKE '{place}';")
    if len(check_unique) != 0 :
        print(a_name,'重複')
        return
    address = data['results'][num]['formatted_address']
    location_x = data['results'][num]['geometry']['location']['lat']
    location_y = data['results'][num]['geometry']['location']['lng']
    try:
        formatted_phone = data_opening_phone[num]['result'].get("formatted_phone_number")
        phone = formatted_phone if formatted_phone is not None else ""
    except:
        phone = ""
    # tags = data['results'][num]['types']
    try:
        opening = data_opening_phone[num]['result']["opening_hours"]["weekday_text"]
    except:
        opening = '{}'
    rating = data['results'][num]['rating']
    score = 0
    try:
        stay_time = sum(data_crowd[num]['time_spent']) // len(data_crowd[num]['time_spent'])
    except:
        stay_time = 0
    hot_month = [1,2,3,4,5,6,7,8,9,10,11,12]
    input_column = ["place",  "photo",  "a_name",  "address",  "location_x",  "location_y",  "phone",  "opening",  "rating",  "score",  "stay_time",  "hot_month"]
    s_len = ('%s,'* len(input_column))[:-1]
    sql = f"INSERT INTO myapp_attractions ({','.join(input_column)}) VALUES ({s_len})"
    print(a_name,'放入資料庫')
    tool.create_multi(sql,[(place,  photo,  a_name,  address,  location_x,  location_y,  phone,  opening,  rating,  score,  stay_time,  hot_month)])

# def get_type(data):

with open('臺北市區路段資料.csv',newline='',encoding='utf-8')as csvfile:
    address_list = list(csv.reader(csvfile))
    list(address_list)
    print(address_list)
    for address in address_list:
        try:
            with open(f'{address[0]}{address[1]}景點.json', encoding='utf-8') as file:
                data = json.load(file)

            with open(f'{address[0]}{address[1]}景點擁擠資訊.json', encoding='utf-8') as file:
                data_crowd = json.load(file)

            with open(f'{address[0]}{address[1]}景點營業時間.json', encoding='utf-8') as file:
                data_opening_phone = json.load(file)
                for num in range(len(data['results'])):
                    input_address(data,data_crowd,data_opening_phone,num)
        except:
            print(f'{address[0]}{address[1]} error')
            continue