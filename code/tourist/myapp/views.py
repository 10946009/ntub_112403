from django.shortcuts import render
from datetime import datetime

import googlemaps
import os
import populartimes
from os.path import join, dirname
from dotenv import load_dotenv, find_dotenv
import requests
from .models import *
from django.http import JsonResponse


#管理者首頁
def admin_index(request): 
    return render(request, "admin_index.html")

#管理者登入頁
def admin_login(request):
    return render(request, "admin_login.html")

#管理者管理帳號
def admin_manageuser(request):
    return render(request, "admin_manageuser.html")

#管理者管理評論
def admin_comment(request):
    return render(request, "admin_comment.html")

#首頁
def index(request):
    return render(request, "index.html")

#登入頁
def login(request):
    
    return render(request, "login.html")

#忘記密碼
def forget_passwd(request):

    return render(request, "forget_passwd.html")

#註冊
def register(request):

    return render(request, "register.html")

#搜尋景點
def search(request):

    return render(request, "search.html",locals())

#建立行程
def create(request):
    return render(request, "create.html")

#我的行程(歷史紀錄)
def history(request):
    return render(request, "history.html")

#我的最愛
def favorite(request):
    favorite_list = []
    user_id = request.user.id
    # project = Project.objects.get(id=project_id)
    #找出user的最愛清單的a.id
    favorite_attrations_list= Favorite.objects.filter(u_id=user_id)
    # a.id取出
    for a_id in favorite_attrations_list:
        favorite_list.append(Attractions.objects.filter(id=a_id.a_id).values())
    # favorite_list =
    return render(request, "favorite.html",locals())

#分享行程
def share(request):
    return render(request, "share.html")

#景點資訊
# def attraction_details(request,a_id):
#     return render(request, "attraction_details.html")

def attraction_details(request):
    if request.GET.get('a_id') != None:
        choose_a_id = request.GET.get('a_id')  # 提取传递的值
        choose_attractions = Attractions.objects.filter(id=choose_a_id).values().first()
        return JsonResponse(choose_attractions)

    keyword_attrations_id = [1,2,3]
    search_list = []
    for a_id in keyword_attrations_id:
        search_list.append(Attractions.objects.filter(id=a_id).values())    
    return render(request, "attraction_details.html",locals())