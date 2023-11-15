from django.shortcuts import render, redirect
from myapp.models import *
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

@login_required(login_url="/login")
def save_attractions_comment(request,aid=None):
    print(request.POST)
    if aid:
        aid = aid
    else:
        aid = request.POST.get("aid")
    user_id = request.user.id
    comment = request.POST.get("comment")
    print(request.POST)
    if comment:
        unit = AttractionsComment.objects.create(u_id=user_id, a_id=aid, content=comment)
        unit.save()
    return JsonResponse({"response_data": "成功"})

@login_required(login_url="/login")
def save_travel_comment(request,cid=None):
    if cid:
        cid = cid
    else:
        cid = request.POST.get("cid")
    user_id = request.user.id
    comment = request.POST.get("comment")

    if comment:
        unit = TravelComment.objects.create(u_id=user_id, c_id=cid, comment=comment)
        unit.save()
    return redirect(f"/attraction_details/{cid}")

def comment_like(request):
    if request.method == "POST":
        comment_id = request.POST.get("comment_id")
        user_id = request.user.id
        if comment_id:
            if AttractionsCommentFavorite.objects.filter(ac_id=comment_id, u_id=user_id).exists():
                AttractionsCommentFavorite.objects.filter(ac_id=comment_id, u_id=user_id).delete()
                return JsonResponse({"response_data": "成功"})
            unit = AttractionsCommentFavorite.objects.create(ac_id=comment_id, u_id=user_id)
            unit.save()
            return JsonResponse({"response_data": "成功"})
        else:
            return JsonResponse({"response_data": "失敗"})
    else:
        return JsonResponse({"response_data": "失敗"})