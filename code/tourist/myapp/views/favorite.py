from django.shortcuts import render, redirect
from myapp.models import *
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
# 我的最愛
@login_required(login_url="/login")
def favorite(request):
    favorite_list = []
    travel_favorite_list = []

    user_id = request.user.id

    # project = Project.objects.get(id=project_id)
    # 找出user的最愛清單的a.id、ct.id
    attrations_favorite = Favorite.objects.filter(u_id=user_id).values()
    travel_favorite = TravelFavorite.objects.filter(u_id=user_id).values()
    travel_favorite_fit =TravelFavorite.objects.filter(u_id=user_id)
    print('attrations_favorite',attrations_favorite)
    print('travel_favorite',travel_favorite)
    # a.id取出
    for a_id in attrations_favorite:
        favorite_list.append(Attractions.objects.get(id=a_id["a_id"]))
    # ct.id取出


    for ct_id in travel_favorite:
        ct_list = Create_Travel.objects.filter(id=ct_id["ct_id"]).values().first()
        #抓user資料庫
        ct_list['u_id'] = User.objects.get(id=ct_list['u_id']) 
        ct_list['ct_object'] = Create_Travel.objects.get(id=ct_list['id'])
        # 抓place_id
        choiceid= ChoiceDay_Ct.objects.filter(ct_id=ct_list['id']).values().first()
        ctaid = Attractions_Ct.objects.filter(choice_ct_id=choiceid['id']).values().first()
        place_id = Attractions.objects.get(id=ctaid['a_id']).place_id
        ct_list['img']=place_id
        travel_favorite_list.append(ct_list)
    print('travel_favorite_list',travel_favorite_list)
    print('favorite_list',favorite_list)
    
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