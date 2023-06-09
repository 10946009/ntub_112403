from django.shortcuts import render, redirect

from datetime import datetime
import random
import googlemaps
import os
import populartimes
from os.path import join, dirname
from dotenv import load_dotenv, find_dotenv
import requests
from .models import *
from django.http import JsonResponse
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password

from django.core.mail import send_mail

from geopy.distance import geodesic

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path, override=True)  # 設定 override 才會更新變數哦！
GOOGLE_PLACES_API_KEY = os.environ.get("GOOGLE_PLACES_API_KEY")


# 管理者首頁
def admin_index(request):
    return render(request, "admin_index.html")


# 管理者登入頁
def admin_login(request):
    return render(request, "admin_login.html")


# 管理者管理帳號
def admin_manageuser(request):
    return render(request, "admin_manageuser.html")


# 管理者管理評論
def admin_comment(request):
    return render(request, "admin_comment.html")


# 首頁
def index(request):
    return render(request, "index.html")


# 登入頁
def login(request):
    message = ""
    if request.method == "POST":
        print(request.POST)
        email = request.POST["email"]
        password = request.POST["passwd"]
        user = authenticate(request, email=email, password=password)
        print(user)
        if user is not None:
            if user.is_active:
                # 驗證成功，登錄用戶
                auth.login(request, user)
                # 重定向到其他頁面或執行其他操作
                return redirect("/")
        else:
            # 驗證失敗，顯示錯誤信息
            message = "帳號或密碼錯誤"
    return render(request, "login.html", locals())


# 忘記密碼
def forget_passwd(request):
    msg = ""
    if request.method == "POST":
        data = request.POST
        if data["email"]:
            email = data["email"]

            if User.objects.filter(email=email).exists():
                code = random_str()  # 隨機生成驗證碼
                request.session["code"] = code  # 將驗證碼保存到session
                request.session["email"] = email
                print(request.session["code"])
                email_title = f"重設密码，您的驗證碼：【{code}】"
                email_body = f"<p>您的TripFunChill網站驗證碼為</p><h2><b>{code}</b></h2>請勿將這組驗證碼轉寄或提供給任何人。<br>若您沒提出此要求，請立刻更改密碼以防帳號被進一步盜用。<br>TripFunChill團隊敬上</p>"
                send_status = send_mail(
                    email_title,
                    None,
                    "tripfunchill@gmail.com",
                    [
                        data["email"],
                    ],
                    html_message=email_body,
                )
                msg = "驗證碼已發送，請查收郵件"
                return render(request, "reset_passwd.html", locals())

            else:
                msg = "此信箱還沒註冊"
    return render(request, "forget_passwd.html", locals())


def reset_passwd(request):
    msg = ""
    if request.method == "POST":
        data = request.POST
        if data["code"]:
            code = data["code"]  # 獲取傳遞過來的驗證碼
            password = data["passwd"]
            password1 = data["passwd1"]
            if code == request.session["code"]:
                if password == password1:
                    user = User.objects.get(email=request.session["email"])
                    # pwd = make_password(password)
                    user.set_password(password)
                    user.save()
                    del request.session["code"]  # 删除session
                    del request.session["email"]
                    msg = "密码已重置"
                    return redirect("/login")
                else:
                    msg = "密碼輸入不一致"
            else:
                msg = "驗證碼錯誤"
            print(request.session["code"])

    return render(request, "reset_passwd.html", locals())


# 隨機生成驗證碼
def random_str(randomlength=6):
    str = ""
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    length = len(chars) - 1
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


# 註冊
def register(request):
    gneder_list = {"0": "不公開", "1": "男", "2": "女"}
    now = str(datetime.now())
    nowday = now[:10]
    message = ""
    if request.method == "POST":
        u = request.POST or None
        print(u)
        if u:
            if User.objects.filter(email=u["email"]).exists():
                message = "e-mail已被使用過"
            else:
                if u["passwd"] == u["passwd1"]:
                    email = u["email"]
                    passwd = make_password(u["passwd"])
                    username = u["username"]
                    gender = gneder_list[u["gender"]]
                    birthday = u["birthday"]
                    unit = User.objects.create(
                        email=email,
                        password=passwd,
                        username=username,
                        gender=gender,
                        birthday=birthday,
                    )
                    unit.save()
                    return redirect("/login")
                else:
                    message = "密碼輸入不一致"

    return render(request, "register.html", locals())


# 搜尋景點
def search(request):
    return render(request, "search.html", locals())


# 建立行程
def create(request):
    return render(request, "create.html")


# 我的行程(歷史紀錄)
def history(request):
    return render(request, "history.html")


# 我的最愛
def favorite(request):
    favorite_list = []
    user_id = request.user.id
    # project = Project.objects.get(id=project_id)
    # 找出user的最愛清單的a.id
    favorite_attrations_list = Favorite.objects.filter(u_id=user_id)
    # a.id取出
    for a_id in favorite_attrations_list:
        favorite_list.append(Attractions.objects.filter(id=a_id.a_id).values())
    # favorite_list =
    return render(request, "favorite.html", locals())


# 分享行程
def share(request):
    return render(request, "share.html")


# 景點資訊
# def attraction_details(request,a_id):
#     return render(request, "attraction_details.html")


def attraction_details(request):
    search_list = []
    print(request.method)

    if request.method == "POST":
        query = request.POST.get("search-query")
        search_url = "/attraction_details/?query=" + query
        search_list = list(Attractions.objects.filter(a_name__contains=query).values())
    else:
        keyword_attrations_id = [1, 2, 3]
        for a_id in keyword_attrations_id:
            search_list.append(Attractions.objects.filter(id=a_id).values().first())

    if request.GET.get("a_id") != None:
        choose_a_id = request.GET.get("a_id")  # 提取傳遞的值
        choose_attractions = Attractions.objects.filter(id=choose_a_id).values().first()
        return JsonResponse(choose_attractions)

    print(search_list)
    return render(request, "attraction_details.html", locals())

def user_edit(request):

    return render(request, "edit.html")


# 確定營業時間
def check_opening(now_time, week):
    ok_a_list = []
    stay_time = 30
    for a in Crowd_Opening.objects.filter(week=week):
        if "休息" not in a.opening:
            if "24 小時營業" in a.opening:
                ok_a_list.append(a.a_id)
            else:
                for opening in a.opening:
                    opening = opening.replace(" ", "")
                    if now_time >= int(opening[0:2]) * 60 + int(
                        opening[3:5]
                    ) and now_time < int(opening[6:8]) + int(opening[9:]):
                        ok_a_list.append(a.a_id)
                        break
    return ok_a_list


# 確定距離
def check_distance(get_uset_address, a_id_list):
    ok_a_list = []
    for a in Attractions.objects.filter(id__in=a_id_list):
        distance = geodesic(
            (get_uset_address[0], get_uset_address[1]), (a.location_x, a.location_y)
        ).kilometers
        # print(a.a_name,distance)
        if distance <= 0.8:
            ok_a_list.append([a.place_id, a.location_x, a.location_y])
    print(ok_a_list)
    return ok_a_list


def check_distance_placeid(get_uset_address, a_id_list):
    ok_a_list = []
    for a in Attractions.objects.filter(id__in=a_id_list):
        distance = geodesic(
            (get_uset_address[0], get_uset_address[1]), (a.location_x, a.location_y)
        ).kilometers
        # print(a.a_name,distance)
        if distance <= 0.8:
            ok_a_list.append(a.place_id)
    return ok_a_list


def test_input(request):
    client = googlemaps.Client(key=GOOGLE_PLACES_API_KEY)
    now_time = 780
    day = "2023-05-25"
    week = datetime(int(day[0:4]), int(day[5:7]), int(day[8:])).weekday() + 1

    # # 1.先選擇固定的5個景點作為M集合（正常為我們根據使用者輸入的位置去進行推薦。大約為開車30分鐘內會到且有營業的地點）
    # * 有營業
    # o_db = Attractions.objects.get(place_id=o)
    # o_crowd_opening = o_db.crowd_opening_set.filter(week=week).values()

    get_uset_address = (25.093071, 121.5323991)  # 抓使用者位置
    get_all_attractions = check_distance(
        get_uset_address, check_opening(now_time, week)
    )
    print(len(get_all_attractions))
    m_attractions_list = []

    # # 發送距離矩陣請求
    # for a_id in get_all_attractions:
    #     response = client.distance_matrix(
    #         origins=get_uset_address, #使用者位置
    #         destinations = (a_id[1],a_id[2]), #目的地
    #         mode="driving", #開車
    #         units="metric", #公里
    #         avoid="highways", #限制沒有高速公路
    #         language="zh-TW",
    #     )
    #     distance = response["rows"][0]["elements"][0]["distance"]["text"]
    #     duration = response["rows"][0]["elements"][0]["duration"]["text"]
    #     duration_value = response["rows"][0]["elements"][0]["duration"]["value"]
    #     if duration_value <= 1800:
    #         m_attractions_list.append([a_id[0],distance,duration])
    # print("推薦的景點為",m_attractions_list)

    # print(response)
    # ---------------------------------------------------已經抓到時間與距離(上方)
    # 2.選擇一些景點做為O（使用者選擇的景點）
    # 抓取使用者所選的景點ID
    o_attractions_list = [
        "ChIJ45YiuLmuQjQRgmBcRZ0ludA",
        "ChIJlT1_96OuQjQRprDCnnAMObs",
    ]
    near_o = []

    # 抓o周遭的景點
    for o in o_attractions_list:
        o_db = Attractions.objects.get(place_id=o)
        o_x = o_db.location_x
        o_y = o_db.location_y
        near_o += check_distance_placeid((o_x, o_y), check_opening(now_time, week))

    # 去掉o_attractions_list本身
    near_o = list(set(near_o) - set(o_attractions_list))
    print("周遭的景點為", near_o)
    # 3.根據O裡面的景點，利用tag找出相似景點並推薦（組成新的O)
    tags_same_score = []
    tags_same_score_total = []
    p_attractions_list = []

    for n in near_o:
        n_db = Attractions.objects.get(place_id=n)
        for o in o_attractions_list:
            score = 0
            o_db = Attractions.objects.get(place_id=o)
            for tag in n_db.att_type:  # 抓出周遭n的tag(需要修改景點標籤)
                if tag in o_db.att_type:  #
                    score += 1
            tags_same_score.append(score)
        tags_same_score_total.append(tags_same_score)
        tags_same_score = []
    # print("tags_same_score_total:",tags_same_score_total)
    max_i_list = []
    f_max_i_list = []
    for index, i in enumerate(tags_same_score_total):
        max_i_list.append([index, max(i)])
    # print("max_i_list:",max_i_list)
    f_max_i_list = sorted(max_i_list, key=lambda x: x[1], reverse=True)[0:10]
    # print("f_max_i_list:",f_max_i_list)
    if len(near_o) < 3:
        for i in range(len(near_o)):
            p_attractions_list.append(near_o[f_max_i_list[i][0]])
    else:
        for i in range(3):
            p_attractions_list.append(near_o[f_max_i_list[i][0]])
    print("推薦周遭景點的順序:", p_attractions_list)

    # 將使用者在p_attractions_list所選的景點加入O
    user_select_p = []
    user_select_p = p_attractions_list  # 抓使用者所選擇的
    o_attractions_list += user_select_p
    # print(o_attractions_list)
    # 4.將使用者所選擇的所有景點
    #     * 根據使用者提供的資料（喜好）去判斷重複程度（如5個相似，1個相似之類的），沒有的話變成手動給(暫定)，

    #     * 再判斷景點的人潮流量（1-5，5為最高），

    time = now_time // 60
    for o in o_attractions_list:
        o_db = Attractions.objects.get(place_id=o)
        o_crowd_opening = o_db.crowd_opening_set.filter(week=week).values()
        crowd = o_crowd_opening[0]["crowd"]
        opening = o_crowd_opening[0]["opening"]
        try:
            crowd = o_crowd_opening[0]["crowd"][time - 1]
            crowd = crowd_judge(crowd)
        except:
            pass
        #     print(crowd)

        # print("時間:",opening,",擁擠:",crowd)
        # print("這裡",o_crowd_opening)

    #     * 最後使用normalization將兩者的區間變成[0,1]，再賦予他們權重（如0.5、0.5），最後根據分數去排序景點。
    return render(request, "_test.html")


# 判斷人潮程度
def crowd_judge(crowd):
    if crowd >= 80:
        return 5
    elif crowd >= 60:
        return 4
    elif crowd >= 40:
        return 3
    elif crowd >= 20:
        return 2
    elif crowd > 0:
        return 1
    else:
        return 0


# 抓到的時間距離資料(參考用)
# {
#     "destination_addresses": [
#         "111台灣台北市士林區福林路60號",
#         "111台灣台北市士林區菁山路101巷246號",
#         "111台灣台北市士林區 德行東路129巷31號蘭雅公園",
#         "111台灣台北市士林區中山北路七段14巷72-74號天和公園",
#         "111台灣台北市士林區中山北路五段460巷4號士林官邸公園",
#     ],
#     "origin_addresses": ["111台灣台北市士林區至善路一段116巷9號"],
#     "rows": [
#         {
#             "elements": [
#                 {
#                     "distance": {"text": "2.2 公里", "value": 2250},
#                     "duration": {"text": "7 分鐘", "value": 425},
#                     "status": "OK",
#                 },
#                 {
#                     "distance": {"text": "15.2 公里", "value": 15157},
#                     "duration": {"text": "31 分鐘", "value": 1881},
#                     "status": "OK",
#                 },
#                 {
#                     "distance": {"text": "3.8 公里", "value": 3786},
#                     "duration": {"text": "13 分鐘", "value": 799},
#                     "status": "OK",
#                 },
#                 {
#                     "distance": {"text": "4.4 公里", "value": 4372},
#                     "duration": {"text": "14 分鐘", "value": 858},
#                     "status": "OK",
#                 },
#                 {
#                     "distance": {"text": "3.8 公里", "value": 3773},
#                     "duration": {"text": "11 分鐘", "value": 670},
#                     "status": "OK",
#                 },
#             ]
#         }
#     ],
#     "status": "OK",
# }
