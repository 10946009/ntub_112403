from django.shortcuts import render, redirect
from myapp.models import *
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

# 刪除酒吧
# def delete_none_crowd(requests):
#     bar = Attractions.objects.filter(detail="酒吧")
#     for i in bar:
#         crowd = i.get_crowd_opening()
#         for c in crowd:
#             c.delete()
#         i.delete()
#     return JsonResponse({"status": "ok"})

# 轉移至酒吧資料庫
# def delete_none_crowd(requests):
#     bar = Attractions.objects.filter(detail="酒吧")
#     for i in bar:
#         unit = Bar.objects.create(
#             bar_place_id = i.place_id,
#             photo = i.photo,  
#             bar_name = i.a_name,
#             address = i.address,
#             location_x = i.location_x,
#             location_y = i.location_y,
#             phone = i.phone,
#             rating = i.rating,
#             rating_total = i.rating_total,
#             hit =i.hit,
#             stay_time = i.stay_time ,
#             hot_month = i.hot_month,
#             bar_type =i.att_type, 
#             detail = i.detail,
#         )
#         unit.save()
#         for c in i.get_crowd_opening():
#             unit2 = Bar_Crowd_Opening.objects.create(
#                 b_id = unit.id,
#                 week= c.week,
#                 crowd = c.crowd,
#                 opening = c.opening,
#             )
#             unit2.save()
        
#     return JsonResponse({"status": "ok"})

# 描述：針對一家店, 系統作為 出餐系統
# 純演算法的input/ output就好, 畫面陽春即可
# input  目前前面還在等待出餐的數量
# output 平均每道菜 出菜的速度即可

# 假設ABC 三道菜, 每道菜 做的時間用5分鐘為單位, A*2, B*1, C*3.
# 假設前面有2A, 3B, 2C. 該餐聽每五分鐘可以處理 5個單位
# input = 2A*2+3B*1+2C*3 = 13
# 13/5 = 2.6 單位

# 這個情境, 因為前面要等, 所以要推薦B
# 如果  input = 3     3 / 5 <<1
# 可以推薦A or C

def foodtest(request):
    unit = 5 #每單位為5分鐘
    unit_dish = 5 #每5分鐘能處理的單位
    

    if request.method == "POST":
        all_dish = food.objects.all().order_by('id')
        now_dish = request.POST.getlist('dish')#目前在等待處理的菜

        allwait = 0  # 等待單位

        for i in range(0,len(now_dish)):
            allwait +=  all_dish[i].unit * int(now_dish[i])

        allwait = allwait / unit_dish # 為input

        print('allwait',allwait)

        for d in all_dish:
            d.wait = round(((d.unit + allwait) * 5))

        if allwait > 1:
            recommend = all_dish.filter(unit__lte=1)  # 推薦<= 1 的部分
            print(recommend)
        else:
            recommend = all_dish.filter(unit__gt=1).order_by('unit')  # 推薦<= 1 的部分
    # print(wait)

    
    # print(sorted_dict)

    return render(request, "food.html", locals())