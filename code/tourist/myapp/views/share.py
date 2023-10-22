from django.shortcuts import render, redirect
from myapp.models import *
from django.http import JsonResponse
# 分享行程
def share(request):
    user = request.user.id
    all_share_list = []
    # 判斷此user有沒有收藏過
    share_list =  Create_Travel.objects.filter(status=1).values()
    for share in share_list:
        if TravelFavorite.objects.filter(u_id=user, ct_id=share["id"]).exists():
            share['is_favorite']= "1"
        else:
            share['is_favorite']= "0"
        share['u_id'] = User.objects.get(id=share['u_id']) 
        # 抓place_id
        choiceid= ChoiceDay_Ct.objects.filter(ct_id=share['id']).values().first()
        ctaid = Attractions_Ct.objects.filter(choice_ct_id=choiceid['id']).values().first()
        place_id = Attractions.objects.get(id=ctaid['a_id']).place_id
        share['img']=place_id
        all_share_list.append(share)
    print(all_share_list)
    return render(request, "share.html",locals())


# 加入最愛
def add_share(request):
    u_id = request.user.id
    print("u_id",u_id)
    ctid = request.POST.get("ctid")
    if u_id != None:
        if ctid:
            data = Create_Travel.objects.get(u_id=u_id, id=ctid)
            if data.status ==1:
                data.status = 0
                print(data.status)
            else:
                data.status = 1
                print(data.status)
            data.save()
            # 在這裡準備你想要回傳給前端的資料
            response_data = {"message": "操作成功"}
            # user_favorite = list(Favorite.objects.filter(u_id=u_id).values())
            # return JsonResponse({"response_data": response_data, "user_favorite": user_favorite})
            return JsonResponse({"response_data": response_data})
    else:
        response_data = {"message": "尚未登入"}
        return JsonResponse({"response_data": response_data})
    return render(request, "share.html")