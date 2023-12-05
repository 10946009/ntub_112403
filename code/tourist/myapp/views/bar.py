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