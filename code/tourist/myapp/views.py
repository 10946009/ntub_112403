import json
from django.shortcuts import render, redirect
from django.contrib import messages
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
from django.db.models import Q
import threading
from django.conf import settings
from django.core.mail import send_mail
from celery import shared_task
import secrets  # 註冊token
# from myapp.task import *

from geopy.distance import geodesic
from django.contrib.auth.decorators import login_required
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path, override=True)  # 設定 override 才會更新變數哦！
GOOGLE_PLACES_API_KEY = os.environ.get("GOOGLE_PLACES_API_KEY")
ATT_TYPE = {
    "tourist_attraction": 1,
    "point_of_interest": 2,
    "establishment": 3,
    "park": 4,
    "place_of_worship": 5,
    "food": 6,
    "museum": 7,
    "landmark": 8,
    "grocery_or_supermarket": 9,
    "store": 10,
    "restaurant": 11,
    "library": 12,
    "school": 13,
    "jewelry_store": 14,
    "church": 15,
    "cafe": 16,
    "mosque": 17,
    "bakery": 18,
    "home_goods_store": 19,
    "art_gallery": 20,
    "route": 21,
    "hindu_temple": 22,
    "pet_store": 23,
    "movie_theater": 24,
    "amusement_park": 25,
    "zoo": 26,
    "meal_delivery": 27,
    "aquarium": 28,
}
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
    return render(request, "index.html", locals())


def logout(request):
    auth.logout(request)
    return redirect("/")


# 登入頁
def login(request):
    result = 0
    message = ""
    request.session["message"] = ""
    request.session["code_result"] = -1
    if request.method == "GET" and request.headers.get("X-Requested-With"):
        print("hello")
        request.session["code_result"] = request.GET.get("code_result")
        if request.session["code_result"] == "0":
            request.session["message"] = "請輸入帳號密碼"
        elif request.session["code_result"] == "1":
            request.session["message"] = "請輸入驗證碼"
        elif request.session["code_result"] == "2":
            request.session["message"] = "驗證碼錯誤"
        elif request.session["code_result"] == "3":
            request.session["message"] = "正確"

    if request.method == "POST":
        submitted_code = request.POST.get("viewsCode")
        print(submitted_code)
        print(request.method, request.session["code_result"])
        result = 2
        print(request.POST)
        email = request.POST["email"]
        password = request.POST["passwd"]
        user = authenticate(request, email=email, password=password)
        print("user", user)
        if user is not None:
            if user.is_active:
                # 驗證成功，登錄用戶
                auth.login(request, user)
                print(result)
                # 重定向到其他頁面或執行其他操作
                return redirect("/")
            else:
                # 驗證失敗，顯示錯誤信息
                request.session["message"] = "帳號或密碼錯誤"
                result = 1
        else:
            result = 1
            request.session["message"] = "帳號或密碼錯誤"
    message = request.session["message"]
    print("result", result)
    print("message", message)
    print(request.session["code_result"])
    return render(request, "login.html", locals())

# @shared_task
def send_mail_function(email_title, email, email_body):
    try:
        finish_send = send_mail(
            email_title,
            None,
            "tripfunchill@gmail.com",
            [email],
            html_message=email_body,
        )
        if finish_send:
            print(f"Email sent successfully to {email}")
        else:
            print(f"Email sending failed to {email}")
        return finish_send
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False

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
                threading.Thread(target=send_mail_function, args=(email_title, email, email_body)).start()

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
                    verification_token = secrets.token_urlsafe(32)
                    unit = User.objects.create(
                        email=email,
                        password=passwd,
                        username=username,
                        gender=gender,
                        birthday=birthday,
                        verification_token=verification_token,
                    )
                    unit.is_active = False
                    unit.save()
                    email_title = f"註冊信箱驗證："
                    email_body = f"<p>您的TripFunChill註冊驗證連結如下，請點選連結並完成註冊，謝謝!</p><h2><b>http://127.0.0.1:8000/register_verification/{verification_token}</b></h2>TripFunChill團隊敬上</p>"
                    threading.Thread(target=send_mail_function, args=(email_title, email, email_body)).start()

                    return redirect("/login")
                else:
                    message = "密碼輸入不一致"

    return render(request, "register.html", locals())


# 註冊驗證
def register_verification(request, token):
    try:
        user = User.objects.get(verification_token=token)
        user.is_active = True
        user.save()
        msg = "註冊成功!!"
        # 可以在這裡添加一個重定向，告訴用戶驗證成功，並將其導向登錄頁面
        return render(request, "register_msg.html", locals())
    except User.DoesNotExist:
        msg = "註冊失敗(連結失效)"
        # 如果令牌無效，可以顯示一個錯誤消息
        return render(request, "register_msg.html", locals())


# 搜尋景點
def search(request):
    return render(request, "search.html", locals())


# 建立行程首頁
@login_required(login_url="/login")
def create_index(request):
    num = 1
    if request.method == "POST":
        u_id = request.user.id
        name = request.POST["createName"]
        start_day = request.POST["createDate"]
        travel_day = request.POST["createDay"]
        unit = Create_Travel.objects.create(
            ct_name=name,
            start_day=start_day,
            u_id=u_id,
            travel_day=travel_day,
        )
        unit.save()
        return redirect(f"/create/{unit.id}/{num}")
    return render(request, "create_index.html")


# 建立行程
@login_required(login_url="/login")
def create(request, ct_id):
    user_favorite = [4, 6, 9, 10, 15, 16, 18]
    ct_data = Create_Travel.objects.get(id=ct_id)
    choiceday = 1
    try:
        ct_attractions_data = ChoiceDay_Ct.objects.get(ct_id=ct_id, day=choiceday)
        ct_attractions_list = Attractions_Ct.objects.filter(
            choice_ct_id=ct_attractions_data.id
        ).values()
    except:
        ct_attractions_list = []
    print(ct_attractions_list)
    travelday = range(1, ct_data.travel_day + 1)
    name = ct_data.ct_name
    start_day = ct_data.start_day
    week = (
        datetime(int(start_day[0:4]), int(start_day[5:7]), int(start_day[8:])).weekday()
        + 1
    )
    ct_id = ct_data.id

    stay_time = 150
    if request.method == "POST":
        ct_status = request.POST["ct_status"]
        print(ct_status)
        if ct_status == "0":
            get_user_address = list(map(float, request.POST["location"].split(",")))
            nowtime = list(map(int, request.POST["nowtime"].split(":")))
            new_nowtime = nowtime[0] * 60 + nowtime[1]
            # nowtime = int(nowtime[:1])*60 + int(nowtime[3:])
            print(get_user_address)
            print(new_nowtime)

            m = recommend(
                user_favorite, new_nowtime, get_user_address, start_day, stay_time
            )
            m_list = Attractions.objects.filter(place_id__in=m)
            crow_opening_list = []
            for i in m_list:
                m_db = (
                    Crowd_Opening.objects.filter(Q(week=week) & Q(a_id=i.id))
                    .values()
                    .first()
                )
                crow_opening_list.append(m_db)
            m_list = list(m_list.values())
            print(m_list)
            print(crow_opening_list[0])
            return JsonResponse(
                {"m_list": m_list, "crow_opening_list": crow_opening_list}
            )

        if ct_status == "1":
            o_attractions_list = request.POST.getlist("select_aid_list[]")
            print(o_attractions_list)
            nowtime = list(map(int, request.POST["nowtime"].split(":")))
            new_nowtime = nowtime[0] * 60 + nowtime[1]
            o = recommend_near(o_attractions_list, new_nowtime, week, stay_time)
            o_list = Attractions.objects.filter(place_id__in=o)
            o_crow_opening_list = []
            for i in o_list:
                o_db = (
                    Crowd_Opening.objects.filter(Q(week=week) & Q(a_id=i.id))
                    .values()
                    .first()
                )
                o_crow_opening_list.append(o_db)
            o_list = list(o_list.values())
            print(o_list)
            print(o_crow_opening_list[0])
            return JsonResponse(
                {"o_list": o_list, "o_crow_opening_list": o_crow_opening_list}
            )

        if ct_status == "2":
            o_attractions_list = request.POST.getlist("all_select[]")
            print(o_attractions_list)
            nowtime = list(map(int, request.POST["nowtime"].split(":")))
            new_nowtime = nowtime[0] * 60 + nowtime[1]
            final = final_order(
                o_attractions_list, new_nowtime, week, stay_time, user_favorite
            )
            # print('final,我在這!!!!!!!!!!!!!!!!',final)
            # ------主要的
            final_result_list = []
            final_crow_opening_list = []
            for f in final[0]:
                temp = Attractions.objects.filter(place_id=f).values().first()
                final_result_list.append(temp)
            for i in final_result_list:
                f_db = (
                    Crowd_Opening.objects.filter(Q(week=week) & Q(a_id=i["id"]))
                    .values()
                    .first()
                )
                final_crow_opening_list.append(f_db)
            # final_result_list = list(final_result_list)
            # ------剩餘的
            final_remainder_result_list = []
            final_remainder_crow_opening_list = []
            try:
                for fr in final[1]:
                    temp_r = Attractions.objects.filter(place_id=fr).values().first()
                    final_remainder_result_list.append(temp_r)

                for i in final_remainder_result_list:
                    fr_db = (
                        Crowd_Opening.objects.filter(Q(week=week) & Q(a_id=i["id"]))
                        .values()
                        .first()
                    )
                    final_remainder_crow_opening_list.append(fr_db)
                # final_remainder_result_list = list(final_remainder_result_list)
            except:
                pass
            # ------------
            print("final_result_list", final_result_list)
            print("final_crow_opening_list", final_crow_opening_list)
            print("final_remainder_result_list", final_remainder_result_list)
            print(
                "final_remainder_crow_opening_list", final_remainder_crow_opening_list
            )

            return JsonResponse(
                {
                    "final_result_list": final_result_list,
                    "final_crow_opening_list": final_crow_opening_list,
                    "final_remainder_result_list": final_remainder_result_list,
                    "final_remainder_crow_opening_list": final_remainder_crow_opening_list,
                }
            )
        choice_ct_id = -1
        if ct_status == "3":
            print("我進來了")
            get_user_address = list(map(float, request.POST["location"].split(",")))
            nowtime = list(map(int, request.POST["nowtime"].split(":")))
            new_nowtime = nowtime[0] * 60 + nowtime[1]
            unit_query = ChoiceDay_Ct.objects.filter(day=choiceday, ct_id=ct_id)
            if unit_query.exists():
                unit = unit_query.first()
                unit.start_location_x = get_user_address[0]
                unit.start_location_y = get_user_address[1]
                unit.start_time = new_nowtime
            else:
                unit = ChoiceDay_Ct.objects.create(
                    day=choiceday,
                    start_location_x=get_user_address[0],
                    start_location_y=get_user_address[1],
                    start_time=new_nowtime,
                    ct_id=ct_id,
                )
            unit.save()
            choice_ct_id = unit.id
            if request.POST["all_id"] != "":
                all_id = list(map(int, request.POST["all_id"].split(",")))
                for index, id in enumerate(all_id):
                    if index == len(all_id) - 1:
                        distance = 0
                        duration = 0
                    else:
                        id_db = Attractions.objects.get(id=id)
                        id2_db = Attractions.objects.get(id=all_id[index + 1])
                        distance = 2200  # 距離(公尺)
                        duration = 10  # 時間(分鐘)
                        # client = googlemaps.Client(key=GOOGLE_PLACES_API_KEY)
                        # response = client.distance_matrix(
                        #     origins=(id_db.location_x,id_db.location_y), #使用者位置
                        #     destinations = (id2_db.location_x,id2_db.location_y), #目的地
                        #     mode="driving", #開車
                        #     units="metric", #公里
                        #     avoid="highways", #限制沒有高速公路
                        #     language="zh-TW",
                        # )
                        # distance = response["rows"][0]["elements"][0]["distance"]["value"]
                        # duration = response["rows"][0]["elements"][0]["duration"]["value"]//60
                    staytime = id_db.stay_time
                    ct = Attractions_Ct.objects.create(
                        a_start_time=new_nowtime,
                        stay_time=staytime,
                        distance=distance,
                        distance_time=duration,
                        order=index + 1,
                        a_id=id,
                        choice_ct_id=choice_ct_id,
                    )
                    ct.save()
                    new_nowtime += 150

            print("hello")

    return render(request, "create.html", locals())


# 我的行程(歷史紀錄)
@login_required(login_url="/login")
def history(request):
    my_history = []
    user_id = request.user.id
    print(user_id)
    my_history = Create_Travel.objects.filter(u_id=user_id).values()
    print(my_history)
    return render(request, "history.html", locals())


# 我的最愛
@login_required(login_url="/login")
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


@login_required(login_url="/login")
def add_favorite(request):
    u_id = request.user.id
    aid = request.POST.get("aid")
    if u_id != None:
        if aid:
            user_a = Favorite.objects.filter(u_id=u_id, a_id=aid)
            if user_a:
                user_a.delete()
            else:
                unit = Favorite.objects.create(u_id=u_id, a_id=aid)
                unit.save()
            # 在這裡準備你想要回傳給前端的資料
            response_data = {"message": "操作成功"}
            return JsonResponse(response_data)
    else:
        response_data = {"message": "尚未登入"}
        return JsonResponse(response_data)


def attraction_details(request):
    all_type_name = list(ATT_TYPE.keys())
    all_type_name_json = json.dumps(all_type_name)
    print(all_type_name)
    search_list = []
    # print(request.method)
    user = request.user.id
    attractions_search = list(Attractions.objects.values_list("a_name", flat=True))
    attractions_search_json = json.dumps(attractions_search)
    if request.method == "POST":
        query = request.POST.get("searchQuery")
        search_url = "/attraction_details/?query=" + query
        search_list = list(Attractions.objects.filter(a_name__contains=query).values())
    else:  # 後續要改(目前為顯示前3筆
        keyword_attrations_id = [1, 2, 3]
        for a_id in keyword_attrations_id:
            search_list.append(Attractions.objects.filter(id=a_id).values().first())
    search_list = search_list[:10]  # 之後要改 目前避免當掉
    if request.GET.get("a_id") != None:
        choose_a_id = request.GET.get("a_id")  # 提取傳遞的值
        choose_attractions = Attractions.objects.filter(id=choose_a_id).values().first()
        return JsonResponse(choose_attractions)

    # 判斷是否已收藏
    for index, search in enumerate(search_list):
        if Favorite.objects.filter(u_id=user, a_id=search["id"]).exists():
            search_list[index].setdefault("is_favorite", "1")
        else:
            search_list[index].setdefault("is_favorite", "0")
    print(search_list)
    return render(request, "attraction_details.html", locals())


def user_edit(request):
    return render(request, "edit.html")


# ------------------------------------確定營業時間(推薦時)
def check_opening(now_time, week, stay_time):
    ok_a_list = []
    now_time += stay_time
    for a in Crowd_Opening.objects.filter(week=week):
        if "休息" not in a.opening:
            if "24小時營業" in a.opening:
                ok_a_list.append(a.a_id)
            else:
                for opening in a.opening:
                    opening = opening.replace(" ", "")
                    if now_time >= int(opening[0:2]) * 60 + int(
                        opening[3:5]
                    ) and now_time <= int(opening[6:8]) * 60 + int(opening[9:]):
                        ok_a_list.append(a.a_id)
                        break
    return ok_a_list


# ------------------------------------確定距離(傳place_id、座標)
def check_distance(get_user_address, a_id_list):
    ok_a_list = []
    for a in Attractions.objects.filter(id__in=a_id_list):
        distance = geodesic(
            (get_user_address[0], get_user_address[1]), (a.location_x, a.location_y)
        ).kilometers
        # print(a.a_name,distance)
        if distance <= 0.8:
            ok_a_list.append([a.place_id, a.location_x, a.location_y])
    print(ok_a_list)
    return ok_a_list


# ------------------------------------確定距離(傳place_id)
def check_distance_placeid(get_user_address, a_id_list):
    ok_a_list = []
    for a in Attractions.objects.filter(id__in=a_id_list):
        distance = geodesic(
            (get_user_address[0], get_user_address[1]), (a.location_x, a.location_y)
        ).kilometers
        # print(a.a_name,distance)
        if distance <= 0.8:
            ok_a_list.append(a.place_id)
    return ok_a_list


# ------------------------------------確認營業時間(排序景點)沒有用到~~~~
def order_check_opening(o_attractions_list, now_time, week):
    ok_a_list = []
    now_time += 150
    for a in Crowd_Opening.objects.filter(week=week):
        if "休息" not in a.opening:
            if "24小時營業" in a.opening:
                ok_a_list.append(a.a_id)
            else:
                for opening in a.opening:
                    opening = opening.replace(" ", "")
                    if now_time >= int(opening[0:2]) * 60 + int(
                        opening[3:5]
                    ) and now_time < int(opening[6:8]) * 60 + int(opening[9:]):
                        ok_a_list.append(a.a_id)
                        break
    return ok_a_list


# ------------------------------------景點排序(根據使用者喜好、擁擠、營業時間)
def order_check_attrations(
    o_attractions_list, now_time, week, stay_time, user_favorite
):
    print("now_time", now_time)
    # 判斷當下有沒有營業，沒有就不放進陣列
    ok_a_list = []
    # now_time+=stay_time
    for o in o_attractions_list:
        o_db = Attractions.objects.get(place_id=o)
        o_crowd_opening = o_db.crowd_opening_set.filter(week=week).values()
        opening = o_crowd_opening[0]["opening"]
        for op in opening:
            if op == "24小時營業":
                ok_a_list.append(o_db.place_id)
            elif op == "休息":
                continue
            else:
                print(o_db.a_name, now_time, op)
                op = op.replace(" ", "")
                if now_time >= int(op[0:2]) * 60 + int(
                    op[3:5]
                ) and now_time + stay_time <= int(op[6:8]) * 60 + int(op[9:]):
                    ok_a_list.append(o_db.place_id)
                    break
    if ok_a_list == []:
        return ""
    # 4.將使用者所選擇的所有景點
    #     * 根據使用者提供的資料（喜好）去判斷重複程度（如5個相似，1個相似之類的），沒有的話變成手動給(暫定)，
    o_crowd_list = []
    o_favorite_list = []
    o_opening_list = []
    temp_o_opening_list = []

    for o in ok_a_list:
        score = 0
        o_db = Attractions.objects.get(place_id=o)
        for tag in o_db.att_type:  # 抓出周遭n的tag(需要修改景點標籤)
            if tag in user_favorite:  #
                score += 1
        o_favorite_list.append(score)

    # 再判斷景點的人潮流量（1-5，1為最高），判斷營業時間
    time = now_time // 60
    # stay_time = 150
    for o in ok_a_list:
        o_db = Attractions.objects.get(place_id=o)
        o_crowd_opening = o_db.crowd_opening_set.filter(week=week).values()
        crowd = o_crowd_opening[0]["crowd"]
        opening = o_crowd_opening[0]["opening"]
        try:
            crowd = o_crowd_opening[0]["crowd"][time - 1]
            crowd = crowd_judge(crowd)
            o_crowd_list.append(crowd)
        except:
            o_crowd_list.append(0)
        for op in opening:
            # print(op)
            if op == "24小時營業":
                o_opening_list.append(1440)
            else:
                op = op.replace(" ", "")
                # 超過150分鐘就減自己，沒有的話就減150
                if o_db.stay_time > stay_time:
                    o_opening_list.append(
                        int(op[6:8]) * 60 + int(op[9:]) - o_db.stay_time
                    )
                else:
                    o_opening_list.append(int(op[6:8]) * 60 + int(op[9:]) - stay_time)
            break
        # o_opening_list.append(temp_o_opening_list)
        temp_o_opening_list = []
    print("ok_a_list", ok_a_list)
    print("o_opening_list", o_opening_list)

    # print("o_crowd_list:",o_crowd_list)
    # print("o_favorite_list:",o_favorite_list)

    o_list = {
        "o_favorite_list": o_favorite_list,
        "o_crowd_list": o_crowd_list,
        "o_opening_list": o_opening_list,
    }
    df = pd.DataFrame(o_list)
    df["total"] = 0
    print("df", df)
    df_html = df.to_html()
    # 標準化 使值在[0,1]之間
    scaler = MinMaxScaler(feature_range=(0, 1)).fit(df)
    X_scaled = scaler.transform(df)
    df_x = pd.DataFrame(X_scaled)

    df_x[3] = (
        df_x[0].mul(0.2) + df_x[1].mul(0.4) + (1 - df_x[2]).mul(0.4)
    )  # 將值皆乘0.5相加後放入total欄位
    print("df_x", df_x)
    df_x_html = df_x.to_html()
    total_list = df_x[3].values.tolist()  # 將df_x[3]的值轉成list
    final = [
        [ok_a_list[x], total_list[x]] for x in range(len(total_list))
    ]  # 將place_id和分數合併
    f_final_list = sorted(final, key=lambda x: x[1], reverse=True)  # 排序
    print("f_final_list", f_final_list)
    f_final_list_name = [
        [
            Attractions.objects.get(place_id=x[0]).a_name,
            Attractions.objects.get(place_id=x[0])
            .crowd_opening_set.filter(week=week)
            .values()[0]["opening"],
        ]
        for x in f_final_list
    ]  # name的List
    # print("時間:",opening,",擁擠:",crowd)
    # print("這裡",o_crowd_opening)
    #     * 最後使用normalization將兩者的區間變成[0,1]，再賦予他們權重（如0.5、0.5），最後根據分數去排序景點。
    return f_final_list[0][0]


# ------------------------------------第1步驟(推薦周遭景點)
def recommend(user_favorite, now_time, get_user_address, day, stay_time):
    client = googlemaps.Client(key=GOOGLE_PLACES_API_KEY)
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


# ------------------------------------第2步驟(推薦相似景點)
def recommend_near(o_attractions_list, now_time, week, stay_time):
    # 2.選擇一些景點做為O（使用者選擇的景點）
    # 抓取使用者所選的景點ID

    # o_attractions_list_name = [
    #     "華山1914文化創意產業園區",
    #     "URS27-華山大草原",
    # ]
    near_o = []
    # 相似標籤

    # 抓o周遭的景點
    for o in o_attractions_list:
        o_db = Attractions.objects.get(place_id=o)
        o_x = o_db.location_x
        o_y = o_db.location_y
        near_o += check_distance_placeid(
            (o_x, o_y), check_opening(now_time, week, stay_time)
        )

    # 去掉o_attractions_list本身
    near_o = list(set(near_o) - set(o_attractions_list))
    print("先前所選的景點為", o_attractions_list)
    print("周遭的景點為", near_o)
    # 3.根據O裡面的景點，利用tag找出相似景點並推薦（組成新的O)
    tags_same_score = []
    tags_same_score_total = []
    p_attractions_list = []
    # -----------------根據type，推薦相似的景點
    for n in near_o:
        n_db = Attractions.objects.get(place_id=n)
        for o in o_attractions_list:
            score = 0
            o_db = Attractions.objects.get(place_id=o)
            # 新增相似標籤------------------!!!!!!
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
    if len(near_o) < 5:
        for i in range(len(near_o)):
            p_attractions_list.append(near_o[f_max_i_list[i][0]])
    else:
        for i in range(5):
            p_attractions_list.append(near_o[f_max_i_list[i][0]])
    near_o = list(set(near_o) - set(p_attractions_list))
    # --------------根據組合，推薦類似type的景點
    o_type = []  # 宣告相似組合的陣列
    tags_same_score_total = []
    for o in o_attractions_list:
        o_db = Attractions.objects.get(place_id=o)
        for a_tag in o_db.att_type:
            for i in ATT_TYPE_LIST:
                if a_tag == i[0]:
                    for x in i:
                        o_type.append(x)
    o_type = list(set(o_type))
    for n in near_o:
        n_db = Attractions.objects.get(place_id=n)
        score = 0
        for tag in n_db.att_type:  # 抓出周遭n的tag(需要修改景點標籤)
            if tag in o_type:  #
                score += 1
        tags_same_score_total.append(score)
    print("tags_same_score_total:", tags_same_score_total)
    max_i_list = []
    f_max_i_list = []
    for index, i in enumerate(tags_same_score_total):
        max_i_list.append([index, i])
    # print("max_i_list:",max_i_list)
    f_max_i_list = sorted(max_i_list, key=lambda x: x[1], reverse=True)[0:10]
    # print("f_max_i_list:",f_max_i_list)
    if len(near_o) < 5:
        for i in range(len(near_o)):
            p_attractions_list.append(near_o[f_max_i_list[i][0]])
    else:
        for i in range(5):
            p_attractions_list.append(near_o[f_max_i_list[i][0]])
    print("推薦相似景點的順序:", p_attractions_list)
    p_attractions_list = [
        Attractions.objects.get(place_id=x).place_id for x in p_attractions_list
    ]  # name的List

    return p_attractions_list


# ------------------------------------第3步驟(最後的排序)
def final_order(o_attractions_list, now_time, week, stay_time, user_favorite):
    final_list = []
    remainder_list = []
    all_list = []
    while len(o_attractions_list) > 0:
        temp = order_check_attrations(
            o_attractions_list, now_time, week, stay_time, user_favorite
        )
        if temp == "":
            break
        final_list.append(temp)
        now_time += stay_time
        o_attractions_list = list(set(o_attractions_list) - set(final_list))
    remainder_list = [
        Attractions.objects.get(place_id=x).place_id
        # Attractions.objects.get(place_id=x).crowd_opening_set.filter(week=week).values()[0]["opening"],
        for x in o_attractions_list
    ]
    # f_final_list_name = [
    #     Attractions.objects.get(place_id=x).place_id
    #     # Attractions.objects.get(place_id=x).crowd_opening_set.filter(week=week).values()[0]["opening"],
    #     for x in final_list
    # ]
    print("final_list!!!!!!!!!!!!!", final_list)
    all_list.append(final_list)
    all_list.append(remainder_list)
    return all_list


def test_input(request):
    # ----------------------------------------------------------------------------------------------------------------
    # print(m_attractions_list_name)
    # print(response)
    m_attractions_list_name = [
        "中央藝文公園",
        "URS27-華山大草原",
        "華山1914文化創意產業園區",
        "忠孝公園",
        "齊東公園",
        "齊東老街",
        "台灣公路原點",
    ]
    # ---------------------------------------------------已經抓到時間與距離(上方)
    # print(o_attractions_list)

    # 將使用者在p_attractions_list所選的景點加入O
    # user_select_p = []
    # user_select_p = p_attractions_list[5:]  # 抓使用者所選擇的
    # o_attractions_list += user_select_p
    # final_o_attractions_list_aid = [
    #     Attractions.objects.get(place_id=x).place_id for x in o_attractions_list
    # ]  # name的List
    # ---------------------排序
    return render(request, "_test.html", locals())


def resort(nowtime, now_list, last_a_list):
    if len(last_a_list) == 0:
        return now_list
    # 確認時間
    # 把當前時間ok的放進now_list
    # 遞迴resort()


# 判斷人潮程度
def crowd_judge(crowd):
    if crowd >= 80:
        return 1
    elif crowd >= 60:
        return 2
    elif crowd >= 40:
        return 3
    elif crowd >= 20:
        return 4
    elif crowd > 0:
        return 5
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


# 我的行程(歷史紀錄)
def sayhello(request):
    return render(request, "_sayhello.html")
