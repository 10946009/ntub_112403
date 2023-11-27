from django.shortcuts import render, redirect,HttpResponse
from myapp.models import *
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime


# 行程詳細頁面
def travel_detail(request,ctid):
    
    if ctid != None:
        u_id = request.user.id
        ct_detail = Create_Travel.objects.get(id=ctid)
        date_string = ct_detail.start_day
        date_object = datetime.strptime(date_string, '%Y-%m-%d')
        # 使用 %u 取得星期的數字表示（1 表示星期一，2 表示星期二，以此類推，7 表示星期日）
        week = int(date_object.strftime('%u'))
        print('week',week)
        if ct_detail.status or u_id==ct_detail.u_id:
            print("有分享或我是作者~~")
            print('ct_detail',ct_detail)
            ct_choiceday = ChoiceDay_Ct.objects.filter(ct_id=ct_detail.id).values()
            print('ct_choiceday',ct_choiceday)
            ct_attraction = []
            for day in ct_choiceday:
                attraction = Attractions_Ct.objects.filter(choice_ct_id=day['id']).order_by('order')
                for a in attraction:
                    a.opening = Crowd_Opening.objects.get(a_id=a.a_id,week=week)
                ct_attraction.append(attraction)
                week = (week + 1) % 8 + 1
            print('ct_attraction',ct_attraction)
        else:
            print("HI")
            return HttpResponse("<h1>Page was found</h1>")
        
        all_data = []
        for ct_choiceday, ct_attraction in zip(ct_choiceday,ct_attraction):
            all_data.append({
                'ct_choiceday': ct_choiceday,
                'ct_attraction': ct_attraction,
            })
    return render(request, "travel_detail.html", locals())