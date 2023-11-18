import json
from django.shortcuts import render, redirect
from myapp.models import *
from django.http import JsonResponse
from .viewsConst import ATT_TYPE_CHINESE

def user_edit(request):
    detail = User.objects.get(id=request.user.id)
    all_type_name = ATT_TYPE_CHINESE
    
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