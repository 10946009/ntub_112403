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