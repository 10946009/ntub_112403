import os
from os.path import join, dirname
from dotenv import load_dotenv, find_dotenv

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path, override=True)  # 設定 override 才會更新變數哦！
GOOGLE_PLACES_API_KEY = os.environ.get("GOOGLE_PLACES_API_KEY")
ATT_TYPE = {
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
}
ATT_TYPE_CHINESE= [
    { 'name': '機構', 'id': 3 },
    { 'name': '公園', 'id': 4 },
    { 'name': '宗教場所', 'id': 5 },
    { 'name': '食物', 'id': 6 },
    { 'name': '博物館', 'id': 7 },
    { 'name': '地標;標誌性建築', 'id': 8 },
    { 'name': '雜貨店或超市', 'id': 9 },
    { 'name': '商店', 'id': 10 },
    { 'name': '餐廳', 'id': 11 },
    { 'name': '圖書館', 'id': 12 },
    { 'name': '學校', 'id': 13 },
    { 'name': '珠寶店', 'id': 14 },
    { 'name': '咖啡廳', 'id': 16 },
    { 'name': '清真寺', 'id': 17 },
    { 'name': '麵包店', 'id': 18 },
    { 'name': '家居商品商店', 'id': 19 },
    { 'name': '藝術', 'id': 20 },
    { 'name': '夜景', 'id': 21 },
    { 'name': '印度教寺廟', 'id': 22 },
    { 'name': '寵物店', 'id': 23 },
    { 'name': '電影院', 'id': 24 },
    { 'name': '遊樂園', 'id': 25 },
    { 'name': '動物園', 'id': 26 },
    { 'name': '水族館', 'id': 28 },
    { 'name': '花', 'id': 29 },
    { 'name': '自然特徵', 'id': 30 },
    { 'name': '夜市', 'id': 31 },
    { 'name': '體育', 'id': 32 },
    { 'name': '露營地', 'id': 33 },
    { 'name': '購物商場', 'id': 34 },
    { 'name': '電子商店', 'id': 35 },
    { 'name': '溫泉', 'id': 36 },
    { 'name': 'DIY', 'id': 37 }
]
ATT_TYPE_LIST = [
    [4, 25, 26, 28, 37],
    [5, 8, 15, 17, 22],
    [6, 9, 10, 11, 16, 18, 19, 31],
    [7, 8, 13, 20, 24, 28],
    [8, 7, 13, 20, 24, 28, 30],
    [9, 6, 10, 14, 19, 34, 35],
    [10, 6, 9, 14, 19, 31, 34, 35],
    [11, 6, 9, 10, 16, 18, 19, 31],
    [12, 7, 8, 13, 20],
    [13, 7, 8, 12, 20],
    [14, 9, 10, 19, 34, 35],
    [15, 5, 8, 17, 22],
    [16, 6, 11, 18],
    [17, 5, 8, 15, 22],
    [18, 6, 11, 16],
    [19, 6, 9, 10, 14, 34, 35],
    [20, 7, 8, 24, 28, 37],
    [21, 8, 29, 30, 33, 36],
    [22, 5, 8, 15, 17],
    [23, 9, 10, 19, 26],
    [24, 7, 8, 20, 28, 37],
    [25, 4, 6, 11, 26, 28],
    [26, 4, 7, 23, 28],
    [28, 4, 7, 23, 26],
    [29, 8, 30, 33, 36],
    [30, 8, 29, 33, 36],
    [31, 6, 10, 11, 19, 21],
    [32, 4, 13, 30, 33],
    [33, 4, 13, 30, 32],
    [34, 6, 10, 11, 14, 16, 19, 35],
    [35, 6, 9, 10, 11, 19],
    [36, 8, 29, 30, 33],
    [37, 4, 7, 20, 24, 25, 26, 28],
]

