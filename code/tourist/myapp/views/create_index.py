
from django.shortcuts import render, redirect
from myapp.models import *
from django.contrib.auth.decorators import login_required
# 建立行程首頁
@login_required(login_url="/login")
def create_index(request):
    num = 1
    if request.method == "POST":
        u_id = request.user.id
        name = request.POST["createName"]
        start_day = request.POST["createDate"]
        travel_day = request.POST["createDay"]
        unit = Create_Travel.objects.create(
            ct_name=name,
            start_day=start_day,
            u_id=u_id,
            travel_day=travel_day,
        )
        unit.save()
        return redirect(f"/create/{unit.id}")
    return render(request, "create_index.html")
