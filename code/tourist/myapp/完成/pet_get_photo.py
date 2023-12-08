import psycopg2
from sqltool import Postgres
import os
import csv
import json
import requests

from os.path import join, dirname
from dotenv import load_dotenv, find_dotenv

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path, override=True)  # 設定 override 才會更新變數
GOOGLE_PLACES_API_KEY = os.environ.get("GOOGLE_PLACES_API_KEY")


def check_file_in_folder(folder_path, file_name):
    file_path = os.path.join(folder_path, file_name)
    return os.path.exists(file_path)

count =0
tool = Postgres()
with open("臺北市區路段資料.csv", newline="", encoding="utf-8") as csvfile:
    address_list = list(csv.reader(csvfile))
    list(address_list)      
    all_place_list = tool.read("SELECT place_id FROM myapp_attractions")
    all_place_list = [x[0] for x in all_place_list]
    for address in address_list[2:]:
        with open(f"{address[0]}{address[1]}景點營業時間.json", encoding="utf-8") as file:
            data_opening_phone = json.load(file)
            for data in data_opening_phone:
                place_id = data["result"]["place_id"]
                try:
                    photo_list = data["result"]["photos"]
                    if place_id in all_place_list:
                        for num in range(len(photo_list)):
                            if check_file_in_folder(f'{os.getcwd()}\\照片\\備份\\',f'{place_id}_{num+1}.jpg'): continue
                            photo_reference = photo_list[num]["photo_reference"]
                            # print(photo_list[num]["photo_reference"])
                            # print(f'{os.getcwd()}\\照片\\{place_id}_{num+1}.jpg')
                            count+=1
                            # ------------------------------------------------------------------
                            max_width = 1024  # 设置所需的最大宽度
                            max_height = 1024  # 设置所需的最大高度
                            # 构建请求URL，包括maxwidth和maxheight参数
                            print(data["result"]["name"])
                            url = f"https://maps.googleapis.com/maps/api/place/photo?photoreference={photo_reference}&maxwidth={max_width}&maxheight={max_height}&key={GOOGLE_PLACES_API_KEY}"
                            # 将your_api_key替换为您的实际API密钥

                            # # 发送HTTP请求获取照片
                            response = requests.get(url)
                            
                            # # 将照片保存到文件
                            with open(f'{os.getcwd()}\\照片\\備份\\{place_id}_{num+1}.jpg', "wb") as file:
                                file.write(response.content) 
                        all_place_list.remove(place_id)    
                except:
                    print(data["result"]["name"],"沒有照片")
                
#opendata的營業時間
with open(f"opendata營業時間.json", encoding="utf-8") as open_file:
    opendata_opening_phone = json.load(open_file)
    for data in opendata_opening_phone:
        place_id = data["result"]["place_id"]
        try:
            photo_list = data["result"]["photos"]
            if place_id in all_place_list:
                for num in range(len(photo_list)):
                    if check_file_in_folder(f'{os.getcwd()}\\照片\\備份\\',f'{place_id}_{num+1}.jpg'): continue
                    photo_reference = photo_list[num]["photo_reference"]
                    print(photo_list[num]["photo_reference"])
                    print(f'{os.getcwd()}\\照片\\{place_id}_{num+1}.jpg')
                    count+=1
                    # ------------------------------------------------------------------
                    max_width = 1024  # 设置所需的最大宽度
                    max_height = 1024  # 设置所需的最大高度
                    # 构建请求URL，包括maxwidth和maxheight参数
                    print(data["result"]["name"])
                    url = f"https://maps.googleapis.com/maps/api/place/photo?photoreference={photo_reference}&maxwidth={max_width}&maxheight={max_height}&key={GOOGLE_PLACES_API_KEY}"
                    # 将your_api_key替换为您的实际API密钥

                    # # 发送HTTP请求获取照片
                    response = requests.get(url)

                    # # 将照片保存到文件
                    with open(f'{os.getcwd()}\\照片\\備份\\{place_id}_{num+1}.jpg', "wb") as file:
                        file.write(response.content)
                all_place_list.remove(place_id)
        except:
            print(data["result"]["name"],"沒有照片")


print(count)