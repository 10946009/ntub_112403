from django.shortcuts import render, redirect
from myapp.models import *
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
# 我的最愛
@login_required(login_url="/login")
def favorite(request):
    favorite_list = []
    user_id = request.user.id
    # project = Project.objects.get(id=project_id)
    # 找出user的最愛清單的a.id
    favorite_attrations_list = Favorite.objects.filter(u_id=user_id).values()
    print(favorite_attrations_list)
    # a.id取出
    for a_id in favorite_attrations_list:
        favorite_list.append(Attractions.objects.get(id=a_id["a_id"]))
    # favorite_list =
    return render(request, "favorite.html", locals())

@login_required(login_url="/login")
def del_favorite(request,a_id):
    u_id = request.user.id
    if u_id != None:
        if a_id:
            data = Favorite.objects.get(u_id=u_id, a_id=a_id)
            data.delete()
            return redirect("/favorite")
    else:
        response_data = {"message": "尚未登入"}
        return JsonResponse(response_data)
    

    
# @login_required(login_url="/login")
def add_favorite(request):
    u_id = request.user.id
    print("u_id",u_id)
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
            user_favorite = list(Favorite.objects.filter(u_id=u_id).values())
            return JsonResponse({"response_data": response_data, "user_favorite": user_favorite})
    else:
        response_data = {"message": "尚未登入"}
        return JsonResponse({"response_data": response_data})
