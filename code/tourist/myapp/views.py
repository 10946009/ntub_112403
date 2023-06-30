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
                email_title = "重設密码"
                code = random_str()  # 隨機生成驗證碼
                request.session["code"] = code  # 将驗證碼保存到session
                request.session["email"] = email
                print(request.session["code"])
                email_body = f"<p>您的TripFunChill網站驗證碼為</p><h2><b>{code}</b></h2>請勿將這組驗證碼轉寄或提供給任何人。<br>若您沒提出此要求，請立刻更改密碼以防帳號被進一步盜用。<br>TripFunChill團隊敬上</p>"
                send_status = send_mail(
                    email_title,
                    None,
                    "tripfunchill@gmail.com",
                    [
                        data["email"],
                    ],
                    html_message= email_body,
                )
                msg = "验证码已发送，请查收邮件"
                return render(request, "reset_passwd.html", locals())

            else:
                msg = "此信箱還沒註冊"
    return render(request, "forget_passwd.html", locals())


def reset_passwd(request):
    msg = ""
    if request.method == "POST":
        data = request.POST
        if data["code"]:
            code = data["code"]  # 获取传递过来的验证码
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
        choose_a_id = request.GET.get("a_id")  # 提取传递的值
        choose_attractions = Attractions.objects.filter(id=choose_a_id).values().first()
        return JsonResponse(choose_attractions)

    print(search_list)
    return render(request, "attraction_details.html", locals())
