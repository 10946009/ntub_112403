import psycopg2
import os
import json
from sqltool import Postgres
from os.path import join, dirname
from dotenv import load_dotenv, find_dotenv
import os
import requests
import populartimes
import json
import datetime
dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path, override=True)  # 設定 override 才會更新變數
GOOGLE_PLACES_API_KEY = os.environ.get("GOOGLE_PLACES_API_KEY")


tool = Postgres()
 
def get_all_place_id(tool):
    result = []
    all_place_id = tool.read("SELECT place_id FROM myapp_attractions")
    for place_id in all_place_id:
        result.append(get_new_crowd(place_id[0]))

    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    json_str = json.dumps(result)
    f = open(os.getcwd()+f'擁擠資訊{month}-{day}.json', 'w',encoding='utf-8')
    f.write(json_str)
    f.close()


def get_new_crowd(place_id):

    return populartimes.get_id(GOOGLE_PLACES_API_KEY,place_id)

def check_file_in_folder(folder_path, file_name):
    file_path = os.path.join(folder_path, file_name)
    return os.path.exists(file_path)


def get_picture():
    all_photo_list = tool.read("SELECT place_id,photo,detail FROM myapp_attractions")
    for photo in all_photo_list:
        if photo[2] != "酒吧": continue
        if check_file_in_folder(f'{os.getcwd()}\\酒吧\\',f'{photo[0]}.jpg'): continue
        max_width = 1024  # 设置所需的最大宽度
        max_height = 1024  # 设置所需的最大高度
        # 构建请求URL，包括maxwidth和maxheight参数
        print({photo[0]})
        url = f"https://maps.googleapis.com/maps/api/place/photo?photoreference={photo[1]}&maxwidth={max_width}&maxheight={max_height}&key={GOOGLE_PLACES_API_KEY}"
        # 将your_api_key替换为您的实际API密钥

        # # 发送HTTP请求获取照片
        response = requests.get(url)

        # # 将照片保存到文件
        with open(f"{os.getcwd()}\\酒吧\\{photo[0]}.jpg", "wb") as file:
            file.write(response.content)

get_picture()
# get_all_place_id(tool)