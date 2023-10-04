from django.shortcuts import render, redirect
import random
from myapp.models import *
import threading
from .send_mail import send_mail_function
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
