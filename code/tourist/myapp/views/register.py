
from django.http import JsonResponse
from django.shortcuts import render, redirect
from datetime import datetime
from .send_mail import send_mail_function
from myapp.models import *
from django.contrib.auth.hashers import make_password
import threading
import secrets  # 註冊token
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
                return JsonResponse({"message": message})
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
                    email_body = f"<p>您的TripFunChill註冊驗證連結如下，請點選連結並完成註冊，謝謝!</p><h2><b>http://140.131.114.160/register_verification/{verification_token}</b></h2>TripFunChill團隊敬上</p>"
                    threading.Thread(target=send_mail_function, args=(email_title, email, email_body)).start()

                    return redirect("/login")
                else:
                    message = "密碼輸入不一致"
                    return JsonResponse({"message": message})

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

