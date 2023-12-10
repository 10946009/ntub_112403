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
    all_dish = food.objects.all().order_by('id')

    allwait = 0  # 等待單位
    for d in all_dish:
        allwait +=  d.unit * d.order_num

    allwait = allwait / unit_dish # 為input

    print('allwait',allwait)

    for d in all_dish:
        d.wait = round(((d.unit + allwait) * unit))

    if allwait > 1:
        recommend = all_dish.filter(unit__lte=1)  # 推薦<= 1 的部分
        for d in recommend:
            d.wait = round(((d.unit + allwait) * unit))
    else:
        recommend = all_dish.filter(unit__gt=1).order_by('unit')  # 推薦<= 1 的部分
        for d in recommend:
            d.wait = round(((d.unit + allwait) * unit))

    if request.method == "POST":
        now_dish = request.POST.getlist('dish') #目前點的菜
        table_num = request.POST['table_num'] #桌號

        for i in range(0,len(now_dish)):
            if int(now_dish[i]) != 0:

                # 將所點的菜加入資料表
                unit = managefood.objects.create(table_num=table_num, num=now_dish[i], dish_id=all_dish[i].id)
                unit.save()
                
                # 將目前等待中的數量加上去
                all_dish[i].order_num += int(now_dish[i])
                all_dish[i].save()
        return redirect("/food")

    return render(request, "food.html", locals())



def manageFood(request,orferfilter=None):
    msg = 'All'
    if orferfilter == 1:
        all_order = managefood.objects.filter(status=True).order_by('id')
        msg = '已完成'
    elif orferfilter == 0:
        all_order = managefood.objects.filter(status=False).order_by('id')
        msg = '準備中'
    else:
        all_order = managefood.objects.all().order_by('id')
    return render(request, "manage_food.html", locals())


def finishManageFood(request,orderid):
    # 將訂單狀態改為完成
    order = managefood.objects.get(id=orderid)
    order.status = True
    order.save()

    # 將數量從food資料表中扣除
    dish = food.objects.get(id=order.dish_id)
    dish.order_num -= order.num
    dish.save()

    return redirect("/managefood")