import json
from django.shortcuts import render, redirect
from myapp.models import *
from django.http import JsonResponse
from .viewsConst import ATT_TYPE_CHINESE,GENDER
from django.contrib.auth.hashers import make_password

def user_edit(request):
    message = ""
    detail = User.objects.get(id=request.user.id)
    all_type_name = ATT_TYPE_CHINESE
    if request.method == "POST":
        print(request.POST)
        user = User.objects.get(id=request.user.id)
        old_pwd = request.POST.get('old_pwd')
        new_pwd = request.POST.get('new_pwd')
        new_pwd1 = request.POST.get('new_pwd1')
        if user.check_password(old_pwd):
            if new_pwd == new_pwd1:
                # user.password = make_password(new_pwd)
                # user.save()
                user.set_password(new_pwd)
                user.save()
                return redirect("/login")
            else:
                message = "密碼與確認密碼不相符"
                return render(request, "edit.html",locals())
        else:
            message = "舊密碼輸入錯誤"
            return render(request, "edit.html",locals())

    return render(request, "edit.html",locals())


def user_change_avatar(request):
    if request.method == "POST":
        user = User.objects.get(id=request.user.id)
        user.user_photo = request.POST.get('avatar')
        user.save()
        return JsonResponse({'status': 'ok'})
    else:
        return JsonResponse({'status': 'fail'})
    

def user_edit_form(request):
    if request.method == "POST":
        print(request.POST)
        user = User.objects.get(id=request.user.id)
        user.username = request.POST.get('username')
        user.gender = GENDER[request.POST.get('gender')]
        user.birthday = request.POST.get('birthday')
        user.save()
        return redirect("/useredit")

def change_favorite(request):
    if request.method == "POST":
        type_id = int(request.POST.get('type_id'))
        user = User.objects.get(id=request.user.id)
        status = ""
        if user:
            type_list = user.user_favorite_tag
            print(type_list)
            print(type_id)
            if type_id in type_list:
                status="remove"
                type_list.remove(type_id)
            else:
                status="add"
                type_list.append(type_id)

            user.user_favorite_tag = type_list
            user.edit_tag_status = True
            user.save()
            
            detail = User.objects.get(id=request.user.id)
            all_type_name = ATT_TYPE_CHINESE

            return JsonResponse({'status': status})
        

def user_edit_pwd(request):
    if request.method == "POST":
        print(request.POST)
        user = User.objects.get(id=request.user.id)
        old_pwd = request.POST.get('old_pwd')
        new_pwd = request.POST.get('new_pwd')
        new_pwd1 = request.POST.get('new_pwd1')
        if user.check_password(old_pwd):
            if new_pwd == new_pwd1:
                # user.password = make_password(new_pwd)
                # user.save()
                user.set_password(new_pwd)
                user.save()
                return redirect("/login")
            else:
                message = "密碼與確認密碼不相符"
                return render(request, "edit.html",locals())
        else:
            message = "舊密碼輸入錯誤"
            return render(request, "edit.html",locals())
            return JsonResponse({'status': 'old_pwd_error'})


def change_light(request):
    light = request.POST['light']
    user = User.objects.get(id=request.user.id)
    print(light)
    if light == "1":
        user.page_light = True
    else:
        user.page_light = False
    user.save()
    return JsonResponse({'status': 'ok'})