from django.shortcuts import render, redirect,HttpResponse
from myapp.models import *
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
# 行程詳細頁面
def travel_detail(request,ctid):
    if ctid != None:
        u_id = request.user.id
        ct_detail = Create_Travel.objects.get(id=ctid)
        print(u_id)
        print(ct_detail.u_id)
        print(ct_detail.status)
        if ct_detail.status or u_id==ct_detail.u_id:
            print("有分享或我是作者~~")
            print('ct_detail',ct_detail)
            ct_choiceday = ChoiceDay_Ct.objects.filter(ct_id=ct_detail.id).values()
            print('ct_choiceday',ct_choiceday)
            ct_attraction = []
            for day in ct_choiceday:
                attraction = Attractions_Ct.objects.filter(choice_ct_id=day['id']).order_by('order').values()
                for a in attraction:
                    aid = a['a_id']
                    a['a_id'] = Attractions.objects.get(id=aid)
                ct_attraction.append(attraction)
            print(ct_attraction)
        else:
            print("HI")
            return HttpResponse("<h1>Page was found</h1>")
    return render(request, "travel_detail.html", locals())