from django.shortcuts import render, redirect
from myapp.models import *
from django.contrib import auth
from django.contrib.auth import authenticate

def logout(request):
    auth.logout(request)
    return redirect("/")


# 登入頁
def login(request,code_result=None):
    result = 0
    message = ""
    alert_msg=""
    next="/"
    if request.GET.get('next'):
        next = request.GET.get('next')
        alert_msg = "請先登入!"
    if request.method == "POST":
        code_result=request.POST["code_result"]
        print("code_result",code_result)
        email = request.POST["email"]
        password = request.POST["passwd"]
        user = authenticate(request, email=email, password=password)
        print("user", user)
        if code_result =="0":
            message="請輸入帳號密碼"
        elif code_result=="1":
            message="請輸入驗證碼"
        elif code_result=="2":
            message="驗證碼錯誤"
        elif code_result=="3":
            print(request.POST)
            if user is not None:
                if user.is_active:
                    # 驗證成功，登錄用戶
                    auth.login(request, user)
                    print(result)
                    # 重定向到其他頁面或執行其他操作
                    return redirect(next)
                else:
                    # 驗證失敗，顯示錯誤信息
                    message = "帳號或密碼錯誤"
                    result = 1
            else:
                # 驗證失敗，顯示錯誤信息
                result = 1
                message = "帳號或密碼錯誤"
    print('message',message)
    return render(request, "login.html", locals())
