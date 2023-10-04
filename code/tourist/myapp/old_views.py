# import json
from django.shortcuts import render, redirect
# from django.contrib import messages
# from datetime import datetime
# import random
# import googlemaps
# import os
# import populartimes

# import requests
from .models import *
# from django.http import JsonResponse
# from django.contrib import auth
# from django.contrib.auth import authenticate, login
# from django.contrib.auth.hashers import make_password
# from django.db.models import Q
# import threading
# from django.conf import settings
# from django.core.mail import send_mail
# from celery import shared_task
# import secrets  # 註冊token
# from django.template.loader import render_to_string #頁面轉成html
# # from myapp.task import *

# from geopy.distance import geodesic
# from django.contrib.auth.decorators import login_required
# import pandas as pd
# from sklearn.preprocessing import MinMaxScaler

# from django.forms.models import model_to_dict
# from tourist.myapp.views.viewsConst import GOOGLE_PLACES_API_KEY, ATT_TYPE, ATT_TYPE_CHINESE


# # 管理者首頁
# def admin_index(request):
#     return render(request, "admin_index.html")


# # 管理者登入頁
# def admin_login(request):
#     return render(request, "admin_login.html")


# # 管理者管理帳號
# def admin_manageuser(request):
#     return render(request, "admin_manageuser.html")


# # 管理者管理評論
# def admin_comment(request):
#     return render(request, "admin_comment.html")





# 搜尋景點
def search(request):
    return render(request, "search.html", locals())





# 分享行程
def share(request):
    return render(request, "share.html")


def user_edit(request):
    return render(request, "edit.html")




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
