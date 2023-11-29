from datetime import datetime
from functools import reduce
from operator import itemgetter
from django.shortcuts import render
import googlemaps
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from myapp.models import *
from .viewsConst import GOOGLE_PLACES_API_KEY
from .check_opening import check_opening
from .check_distance import check_distance_placeid
from django.db.models import F,Q,Count

# ------------------------------------第1步驟(推薦周遭景點)
def recommend(user_favorite, now_time, get_user_address, day, stay_time):
    try:
        client = googlemaps.Client(key=GOOGLE_PLACES_API_KEY)
    except:
        client = None
    week = datetime(int(day[0:4]), int(day[5:7]), int(day[8:])).weekday() + 1

    # # 1.先選擇固定的5個景點作為M集合（正常為我們根據使用者輸入的位置去進行推薦。大約為開車30分鐘內會到且有營業的地點）
    # * 有營業
    # o_db = Attractions.objects.get(place_id=o)
    # o_crowd_opening = o_db.crowd_opening_set.filter(week=week).values()

    get_all_attractions = check_distance_placeid(
        get_user_address, check_opening(now_time, week, stay_time)
    )
    # print("get_all_attractions",len(get_all_attractions))
    m_attractions_list = []
    if len(get_all_attractions) == 0 or client == None:  # 抓不到資料的話就回傳熱門景點
        print("回傳熱門景點")
        m_attractions_list = [
            x.place_id for x in Attractions.objects.annotate(result=F('rating') * F('rating_total')).order_by('result')[:10]
        ]
        return m_attractions_list
    locations = {"lat": get_user_address[0], "lng": get_user_address[1]}
    # -------------------------------------發送距離矩陣請求
    # for a_id in get_all_attractions:
    #     response = client.distance_matrix(
    #         origins=locations,  # 使用者位置
    #         destinations=(a_id[1], a_id[2]),  # 目的地
    #         mode="driving",  # 開車
    #         units="metric",  # 公里
    #         avoid="highways",  # 限制沒有高速公路
    #         language="zh-TW",
    #     )
    #     distance = response["rows"][0]["elements"][0]["distance"]["text"]
    #     duration = response["rows"][0]["elements"][0]["duration"]["text"]
    #     duration_value = response["rows"][0]["elements"][0]["duration"]["value"]
    #     if duration_value <= 1800:  # 30分鐘
    #         m_attractions_list.append([a_id[0], distance, duration])
    m_attractions_list = [[x] for x in get_all_attractions]
    m_id = [
        Attractions.objects.get(place_id=x[0]).id for x in m_attractions_list
    ]  # name的List
    m_rating = [
        Attractions.objects.get(place_id=x[0]).rating for x in m_attractions_list
    ]  # name的List
    m_rating_total = [
        Attractions.objects.get(place_id=x[0]).rating_total for x in m_attractions_list
    ]  # name的List
    m_favorite_list = []
    for m in m_attractions_list:
        score = 0
        m_db = Attractions.objects.get(place_id=m[0])
        for tag in m_db.att_type:  # 抓出周遭n的tag(需要修改景點標籤)
            if tag in user_favorite:  #
                score += 1
        m_favorite_list.append(score)

    # --------------------------------------------------標準化和排序
    m_list = {
        "m_rating": m_rating,
        "m_rating_total": m_rating_total,
        "m_favorite_list": m_favorite_list,
    }
    df_m_list = pd.DataFrame(m_list)
    df_m_list["total"] = 0
    df_m_list.index = m_id
    print("df_m_list", df_m_list)
    df_m_list_html = df_m_list.to_html()
    # 標準化 使值在[0,1]之間
    scaler_m = MinMaxScaler(feature_range=(0, 1)).fit(df_m_list)
    X_scaled_m = scaler_m.transform(df_m_list)
    df_x_m_list = pd.DataFrame(X_scaled_m)

    df_x_m_list[3] = (
        df_x_m_list[0].mul(0.35) + df_x_m_list[1].mul(0.35) + df_x_m_list[2].mul(0.3)
    )  # 將值皆乘0.5相加後放入total欄位
    df_x_m_list.index = m_id

    print("df_x_m_list", df_x_m_list)
    df_x_m_list_html = df_x_m_list.to_html()
    total_m_list = df_x_m_list[2].values.tolist()  # 將df_x[2]的值轉成list
    final_m = [
        [m_id[x], total_m_list[x]] for x in range(len(total_m_list))
    ]  # 將place_id和分數合併
    f_final_m_list = sorted(final_m, key=lambda x: x[1], reverse=True)  # 排序
    print("f_final_m_list", f_final_m_list)
    f_final_m_list_place_id = [
        Attractions.objects.get(id=x[0]).place_id
        for x in f_final_m_list  # 可能會換place_id
    ]
    m_attractions_list = f_final_m_list_place_id
    print("推薦的景點為", m_attractions_list)
    m_attractions_list_name = [
        Attractions.objects.get(place_id=x).a_name for x in m_attractions_list
    ]  # name的List

    return m_attractions_list[:10]


# ------------------------------------第1.5步驟(推薦使用者可能喜歡的景點)
def recommend_maybe(userid):  # 會回傳可能喜歡的使用者id和該使用者點擊過的景點object
    # 找出user和其他user的交集景點
    other_user = UserClick.objects.values("u_id").distinct()
    user_click = UserClick.objects.filter(u_id=userid).values_list("a_id", flat=True)
    if user_click:  # 如果使用者有資料
        other_user_click = {}
        for uid in other_user:
            uid = uid["u_id"]
            aid_list = list(
                UserClick.objects.filter(u_id=uid).values_list("a_id", flat=True)
            )
            other_user_click[uid] = aid_list

        other_user_intersection = {}
        for key, other_click in other_user_click.items():  # 取交集數量
            if key == userid:
                continue
            other_user_intersection[key] = len(
                set(user_click).intersection(set(other_click))
            )

        # 轉為list並排序 [0]為uid [1]為交集數量
        other_user_intersection = sorted(
            other_user_intersection.items(), key=lambda x: x[1], reverse=True
        )
        if other_user_intersection:
            if other_user_intersection[0][1] != 0:  # 假設有交集
                maybe_user_id = other_user_intersection[0][0]
                maybe_aid_list = UserClick.objects.filter(u_id=maybe_user_id).values_list(
                    "a_id", flat=True
                )
                return Attractions.objects.filter(id__in=maybe_aid_list).annotate(result=F('rating') * F('rating_total')).order_by('-result')[:5] #回傳可能喜歡的景點

        return Attractions.objects.filter(id__in=user_click)[:5] #回傳使用者點擊過的景點
    else:
        return Attractions.objects.all().order_by("hit")[:5] #回傳熱門景點
    # 找出和其他使用者瀏覽相似的景點

def recommend_user_favorite(userid):
    # 使用者喜歡的標籤
    user_favorite_tag = User.objects.get(id=userid).user_favorite_tag
    if user_favorite_tag:
        user_favorite_set = set(user_favorite_tag)

        # 獲取每個景點的標籤
        attractions = Attractions.objects.all()
        # 計算每個景點標籤與使用者喜歡的標籤的交集長度
        intersections = [(a.id, len(set(a.att_type) & user_favorite_set)) for a in attractions]

        # 按照交集長度降序排序
        sorted_intersections = sorted(intersections, key=itemgetter(1), reverse=True)

        # 取前五個
        top_five_recommendations = sorted_intersections[:5]
        recommended_ids = [x[0] for x in top_five_recommendations]
        top_five = Attractions.objects.filter(id__in=recommended_ids)
    else:
        top_five = Attractions.objects.all().order_by("hit")[:5]
    return top_five #回傳使用者喜歡的標籤的景點