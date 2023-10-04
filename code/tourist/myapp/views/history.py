from django.shortcuts import render, redirect
from myapp.models import *
from django.contrib.auth.decorators import login_required
# 我的行程(歷史紀錄)
@login_required(login_url="/login")
def history(request):
    my_history = []
    user_id = request.user.id
    print(user_id)
    my_history = Create_Travel.objects.filter(u_id=user_id).values()
    print(my_history)
    return render(request, "history.html", locals())