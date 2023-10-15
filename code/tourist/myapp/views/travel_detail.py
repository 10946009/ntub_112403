from django.shortcuts import render, redirect
from myapp.models import *
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
# 行程詳細頁面
def travel_detail(request):
    return render(request, "travel_detail.html", locals())