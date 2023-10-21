from django.shortcuts import render, redirect
from myapp.models import *
from django.http import JsonResponse

def user_edit(request):
    detail = User.objects.get(id=request.user.id)
    return render(request, "edit.html",locals())
