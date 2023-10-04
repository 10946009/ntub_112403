
import json
from django.shortcuts import render
from myapp.models import *
from django.http import JsonResponse
from django.db.models import Q
from django.template.loader import render_to_string #頁面轉成html
from django.forms.models import model_to_dict
from .viewsConst import  ATT_TYPE_CHINESE
def attraction_details(request):
    # # 取得景點名稱
    # all_type_name = list(ATT_TYPE_CHINESE.keys())
    all_type_name_json = json.dumps(ATT_TYPE_CHINESE)
    
    #取得搜尋到的結果
    search_list = []
    user = request.user.id
    attractions_search = list(Attractions.objects.values_list("a_name", flat=True))
    attractions_search_json = json.dumps(attractions_search)

    if request.method == "GET" and request.GET.get("search_text") != None:
        print(request.GET)
        att_type = [request.GET.get("att_type[]")]
        search_text = request.GET.get("search_text")
        # 初始化一个Q对象，表示没有过滤条件
        filter_condition_and = Q()
        filter_condition_or = Q()
        # 如果search_text不为空，添加a_name__contains查询条件
        print(search_text,att_type)
        if search_text:
            filter_condition_and &= Q(a_name__contains=search_text)
            filter_condition_or |= Q(a_name__contains=search_text)
        # 如果att_type不为空，添加att_type__contains查询条件
        if att_type:
            filter_condition_and &= Q(att_type__contains=att_type)
            filter_condition_or |= Q(att_type__contains=att_type)

        search_list_and = list(Attractions.objects.filter(filter_condition_and)[:30].values())
        search_list_or = list(Attractions.objects.filter(filter_condition_or).exclude(filter_condition_and)[:30].values())
        search_list = search_list_and + search_list_or

        html = render_to_string(
            template_name="attraction_details_search.html", 
            context={"search_list": search_list}
        )
        data_dict = {"keyword_search_list": html}

        return JsonResponse(data=data_dict, safe=False)
        
    if request.method == "POST":
        query = request.POST.get("searchQuery")
        search_url = "/attraction_details/?query=" + query
        search_list = list(Attractions.objects.filter(a_name__contains=query).values())
    else:  # 後續要改(目前為顯示前3筆
        keyword_attrations_id = [1, 2, 3]
        for a_id in keyword_attrations_id:
            search_list.append(Attractions.objects.filter(id=a_id).values().first())
    search_list = search_list[:10]  # 之後要改 目前避免當掉
    if request.GET.get("a_id") != None:
        choose_a_id = request.GET.get("a_id")  # 提取傳遞的值
        choose_attractions = Attractions.objects.get(id=choose_a_id)
        choose_attractions.hit +=1
        choose_attractions.save()
        choose_attractions_dict = model_to_dict(choose_attractions)
        print(choose_attractions_dict)
        return JsonResponse(choose_attractions_dict, safe=False)

    # 判斷是否已收藏
    for index, search in enumerate(search_list):
        if Favorite.objects.filter(u_id=user, a_id=search["id"]).exists():
            search_list[index].setdefault("is_favorite", "1")
        else:
            search_list[index].setdefault("is_favorite", "0")
    # print(search_list)
    return render(request, "attraction_details.html", locals())

def attraction_details_att_type(request):
    # 取得景點名稱
    # all_type_name = list(ATT_TYPE_CHINESE.keys())
    all_type_name_json = json.dumps(ATT_TYPE_CHINESE)
    att_type = [request.POST["sure_att_type"]]
    search_list = list(Attractions.objects.filter(att_type__contains=att_type).values())
    print(search_list)
    return render(request, "attraction_details.html", locals())
