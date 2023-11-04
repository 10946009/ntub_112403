import json
from django.shortcuts import render
from myapp.models import *
from django.http import JsonResponse
from django.db.models import Q
from django.template.loader import render_to_string  # 頁面轉成html
from django.forms.models import model_to_dict
from .viewsConst import ATT_TYPE_CHINESE
from .findpicture import get_picture_list

def keyword_search(search_text, filter_condition_and, filter_condition_or, method):
    # Q物件可以用&和|來串接，串接後的Q物件可以用來過濾資料
    if method == "tag_search":
        matching_dict = None
        for item in ATT_TYPE_CHINESE:
            if item.get("name") == search_text:
                matching_dict = item
                break

        if matching_dict:
            search_text = [matching_dict.get("id")]
            print("相符的id是：", search_text)
        else:
            print("未找到相符的字典")
    filter_condition_and &= Q(**{f"{TEX_CALL[method]}__contains": search_text})
    filter_condition_or |= Q(**{f"{TEX_CALL[method]}__contains": search_text})
    return filter_condition_and, filter_condition_or


TEX_CALL = {
    "keyword_search": "a_name",
    "tag_search": "att_type",
}

def search(request):
    if request.method == "GET" and request.GET.get("search_text") != None:
        # 初始化一个Q对象，表示没有过滤条件
        filter_condition_and = Q()
        filter_condition_or = Q()
        search_text = request.GET.get("search_text")
        data_type = request.GET.get("data_type")
        filter_condition_and, filter_condition_or = keyword_search(
                search_text, filter_condition_and, filter_condition_or, data_type
            )
        

        search_list_and = list(
            Attractions.objects.filter(filter_condition_and)[:30].values()
        )
        search_list_or = list(
            Attractions.objects.filter(filter_condition_or)
            .exclude(filter_condition_and)[:30]
            .values()
        )
        search_list = search_list_and + search_list_or

        html = render_to_string(
            template_name="create_search.html",
            context={"search_list": search_list},
        )
        data_dict = {"search_list": html}
        print(search_list)
    else:  # 後續要改(目前為顯示前3筆
        keyword_attrations_id = [1, 2, 3]
        for a_id in keyword_attrations_id:
            search_list.append(Attractions.objects.filter(id=a_id).values().first())

    search_list = search_list[:10]  # 之後要改 目前避免當掉
    
    return JsonResponse(data=data_dict, safe=False)
    