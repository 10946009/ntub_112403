from django.shortcuts import render, redirect
from myapp.models import *
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
# 我的最愛
@login_required(login_url="/login")
def favorite(request):
    user_id = request.user.id

    # 找出user的最愛清單的a.id、ct.id
    favorite_list = Favorite.objects.filter(u_id=user_id)
    travel_favorite_list = TravelFavorite.objects.filter(u_id=user_id)

    return render(request, "favorite.html", locals())

#景點刪除最愛
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
    

#景點加入最愛
# @login_required(login_url="/login")
def add_favorite(request):
    u_id = request.user.id
    print("u_id",u_id)
    aid = request.POST.get("id")
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

# 行程加入最愛
def add_travel_favorite(request):
    u_id = request.user.id
    print("u_id",u_id)
    id = request.POST.get("id")
    if u_id != None:
        if id:
            user_ct = TravelFavorite.objects.filter(u_id=u_id, ct_id=id)
            if user_ct:
                user_ct.delete()
            else:
                unit = TravelFavorite.objects.create(u_id=u_id, ct_id=id)
                unit.save()
            # 在這裡準備你想要回傳給前端的資料
            response_data = {"message": "操作成功"}
            user_favorite = list(Favorite.objects.filter(u_id=u_id).values())
            return JsonResponse({"response_data": response_data, "user_favorite": user_favorite})
    else:
        response_data = {"message": "尚未登入"}
        return JsonResponse({"response_data": response_data})


#景點刪除最愛
@login_required(login_url="/login")
def del_travel_favorite(request,ct_id):
    u_id = request.user.id
    if u_id != None:
        if ct_id:
            data = TravelFavorite.objects.get(u_id=u_id, ct_id=ct_id)
            data.delete()
            return redirect("/favorite")
    else:
        response_data = {"message": "尚未登入"}
        return JsonResponse(response_data)