
from datetime import datetime
import googlemaps
from myapp.models import *
from .viewsConst import GOOGLE_PLACES_API_KEY
from .check_opening import check_opening
from .check_distance import check_distance
# ------------------------------------第1步驟(推薦周遭景點)
def recommend(user_favorite, now_time, get_user_address, day, stay_time):
    # client = googlemaps.Client(key=GOOGLE_PLACES_API_KEY)
    week = datetime(int(day[0:4]), int(day[5:7]), int(day[8:])).weekday() + 1

    # # 1.先選擇固定的5個景點作為M集合（正常為我們根據使用者輸入的位置去進行推薦。大約為開車30分鐘內會到且有營業的地點）
    # * 有營業
    # o_db = Attractions.objects.get(place_id=o)
    # o_crowd_opening = o_db.crowd_opening_set.filter(week=week).values()

    get_user_address = get_user_address  # 抓使用者位置
    get_all_attractions = check_distance(
        get_user_address, check_opening(now_time, week, stay_time)
    )
    print(len(get_all_attractions))
    m_attractions_list = []

    # # -------------------------------------發送距離矩陣請求
    # for a_id in get_all_attractions:
    #     response = client.distance_matrix(
    #         origins=get_user_address, #使用者位置
    #         destinations = (a_id[1],a_id[2]), #目的地
    #         mode="driving", #開車
    #         units="metric", #公里
    #         avoid="highways", #限制沒有高速公路
    #         language="zh-TW",
    #     )
    #     distance = response["rows"][0]["elements"][0]["distance"]["text"]
    #     duration = response["rows"][0]["elements"][0]["duration"]["text"]
    #     duration_value = response["rows"][0]["elements"][0]["duration"]["value"]
    #     if duration_value <= 1800: # 30分鐘
    #         m_attractions_list.append([a_id[0],distance,duration])

    # m_id = [Attractions.objects.get(place_id=x[0]).id for x in m_attractions_list] # name的List
    # m_rating = [Attractions.objects.get(place_id=x[0]).rating for x in m_attractions_list] # name的List
    # m_rating_total = [Attractions.objects.get(place_id=x[0]).rating_total for x in m_attractions_list] # name的List
    # m_favorite_list = []
    # for m in m_attractions_list:
    #     score = 0
    #     m_db = Attractions.objects.get(place_id=m[0])
    #     for tag in m_db.att_type:  # 抓出周遭n的tag(需要修改景點標籤)
    #         if tag in user_favorite:  #
    #             score += 1
    #     m_favorite_list.append(score)

    # # --------------------------------------------------標準化和排序
    # m_list = {"m_rating": m_rating, "m_rating_total": m_rating_total,'m_favorite_list':m_favorite_list}
    # df_m_list = pd.DataFrame(m_list)
    # df_m_list["total"] = 0
    # df_m_list.index = m_id
    # print("df_m_list", df_m_list)
    # df_m_list_html = df_m_list.to_html()
    # # 標準化 使值在[0,1]之間
    # scaler_m = MinMaxScaler(feature_range=(0, 1)).fit(df_m_list)
    # X_scaled_m = scaler_m.transform(df_m_list)
    # df_x_m_list = pd.DataFrame(X_scaled_m)

    # df_x_m_list[3] = df_x_m_list[0].mul(0.35)+df_x_m_list[1].mul(0.35)+df_x_m_list[2].mul(0.3)  # 將值皆乘0.5相加後放入total欄位
    # df_x_m_list.index = m_id

    # print("df_x_m_list", df_x_m_list)
    # df_x_m_list_html = df_x_m_list.to_html()
    # total_m_list = df_x_m_list[2].values.tolist()  # 將df_x[2]的值轉成list
    # final_m = [
    #     [m_id[x], total_m_list[x]] for x in range(len(total_m_list))
    # ]  # 將place_id和分數合併
    # f_final_m_list = sorted(final_m, key=lambda x: x[1], reverse=True)  # 排序
    # print("f_final_m_list", f_final_m_list)
    # f_final_m_list_place_id = [
    #     Attractions.objects.get(id=x[0]).place_id for x in f_final_m_list  #可能會換place_id
    # ]
    # m_attractions_list=f_final_m_list_place_id
    # print("推薦的景點為",m_attractions_list)
    # m_attractions_list_name = [Attractions.objects.get(place_id=x).a_name for x in m_attractions_list] # name的List
    m_attractions_list = [
        "ChIJFZPS7xyrQjQRQuUZYgdk3SA",
        "ChIJXcZNw26yQjQRk-ovoSxin1g",
        "ChIJe7yJbYSpQjQRWKgqXWSDg7w",
        "ChIJQev3766vQjQR_R7YpgCRhLk",
        "ChIJTeIZgaCvQjQRlMvYvVAE6WE",
    ]
    return m_attractions_list