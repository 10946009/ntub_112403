from django.shortcuts import render, redirect
from myapp.models import *
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

@login_required(login_url="/login")
def save_attractions_comment(requests,aid=None):
    if aid:
        aid = aid
    else:
        aid = requests.POST.get("aid")
    user_id = requests.user.id
    comment = requests.POST.get("comment")
    if comment:
        unit = AttractionsComment.objects.create(u_id=user_id, a_id=aid, comment=comment)
        unit.save()
        return redirect("/attraction_details/"+str(aid))
    else:
        return redirect("/attraction_details/"+str(aid))

@login_required(login_url="/login")
def save_travel_comment(requests,cid=None):
    if cid:
        cid = cid
    else:
        cid = requests.POST.get("cid")
    user_id = requests.user.id
    comment = requests.POST.get("comment")
    if comment:
        unit = TravelComment.objects.create(u_id=user_id, c_id=cid, comment=comment)
        unit.save()
        return redirect("/travel_detail/"+str(cid))
    else:
        return redirect("/travel_detail/"+str(cid))