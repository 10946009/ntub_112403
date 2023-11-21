from django.http import JsonResponse
from django.shortcuts import render, redirect
from myapp.models import *
from django.contrib.auth.decorators import login_required

# 我的行程(歷史紀錄)
@login_required(login_url="/login")
def history(request,select=None):
    my_history = []
    user_id = request.user.id
    print(user_id)
    if select==0:
        # 抓出此user的未分享行程資料
        my_history = Create_Travel.objects.filter(u_id=user_id,status=False).order_by('id').values()
    elif select==1:
        # 抓出此user的分享行程資料
        my_history = Create_Travel.objects.filter(u_id=user_id,status=True).order_by('id').values()
    else:
        # 抓出此user的所有行程資料
        my_history = Create_Travel.objects.filter(u_id=user_id).order_by('id').values()
    print('my_history',my_history)
    choiceday_ct = []
    # 抓出ct_id相同的資料(可能會有day1、day2之類的)
    for i in my_history:
        choiceday_ct.append(ChoiceDay_Ct.objects.filter(ct_id=i['id']).values())
    print('choiceday_ct',choiceday_ct)
    # 抓出同一天中的所有景點
    allAttractions = []
    for item in choiceday_ct:
        ct_allattractions_list = []
        temp_allattractions = []
        for i in item:
            temp_allattractions =Attractions_Ct.objects.filter(choice_ct_id=i['id']).order_by('order').values()
            for temp in range(len(temp_allattractions)):
                aid = temp_allattractions[temp]['a_id']
                temp_allattractions[temp]['a_id'] = Attractions.objects.get(id=aid)
            ct_allattractions_list.append(temp_allattractions)
        allAttractions.append(ct_allattractions_list)
    print('allAttractions',allAttractions)
    
    # 合併上面四個資料
    all_data = []
    for my_history, choiceday_ct, allAttractions in zip(my_history, choiceday_ct, allAttractions):
        all_data.append({
            'my_history': my_history,
            'choiceday_ct': choiceday_ct,
            'allAttractions' : allAttractions
        })
    return render(request, "history.html", locals())
# temp_allattractions.filter(id=item['id']).update(a_id=attractions_data)

def travel_info(request):
    print(request.GET)
    ctid = request.GET.get("id")
    u_id = request.user.id
    ct_detail = Create_Travel.objects.get(id=ctid, u_id=u_id)
    if ct_detail:
        return render(request, 'history_detail.html', {'data': ct_detail})
# temp_allattractions.filter(id=item['id']).update(a_id=attractions_data)

def travel_delete(request):
    ctid = request.POST["id"]
    print(ctid)
    ct = Create_Travel.objects.get(id=ctid,u_id=request.user.id)
    if ct:
        ct.delete()
        return JsonResponse({'message': '刪除成功'})
    else:
        return JsonResponse({'message': '刪除失敗'})
    