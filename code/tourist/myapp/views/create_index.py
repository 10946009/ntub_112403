
from django.shortcuts import render, redirect
from myapp.models import *
from django.contrib.auth.decorators import login_required
# 建立行程首頁
@login_required(login_url="/login")
def create_index(request,ispet=None):
    num = 1
    if request.method == "POST":
        u_id = request.user.id
        name = request.POST["createName"]
        start_day = request.POST["createDate"]
        travel_day = request.POST["createDay"]
        createType = request.POST["createType"]
        if createType == "1":
            createType = True
        else:
            createType = False

        unit = Create_Travel.objects.create(
            ct_name=name,
            start_day=start_day,
            u_id=u_id,
            travel_day=travel_day,
            ispet = createType,
        )
        unit.save()
        for i in range(int(travel_day)):
            choice_unit = ChoiceDay_Ct.objects.create(
                ct_id=unit.id,
                day=i+1,
                start_time="540",
                start_location_x="25.04638359",
                start_location_y="121.5174624",
                location_name="台北車站",
            )
        return redirect(f"/create/{unit.id}")
    return render(request, "create_index.html",locals())
