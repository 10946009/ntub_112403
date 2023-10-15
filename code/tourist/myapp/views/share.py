from django.shortcuts import render, redirect
from myapp.models import *
from django.http import JsonResponse
# 分享行程
def share(request):
    return render(request, "share.html")


# 加入最愛
def add_favorite_share(request):
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