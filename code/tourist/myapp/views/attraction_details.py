import json
from django.shortcuts import render
from myapp.models import *
from django.http import JsonResponse
from django.db.models import Q
from django.template.loader import render_to_string  # 頁面轉成html
from django.forms.models import model_to_dict
from .viewsConst import ATT_TYPE_CHINESE


def keyword_search(search_text, filter_condition_and, filter_condition_or, method):
    
    # Q物件可以用&和|來串接，串接後的Q物件可以用來過濾資料
    if method == "tag_search":
        matching_dict = None
        for item in ATT_TYPE_CHINESE:
            if item.get('name') == search_text:
                matching_dict = item
                break

        if matching_dict:
            search_text = [matching_dict.get('id')]
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


def attraction_details(request):
    # # 取得景點名稱
    # all_type_name = list(ATT_TYPE_CHINESE.keys())
    all_type_name_json = json.dumps(ATT_TYPE_CHINESE)

    # 取得搜尋到的結果
    search_list = []
    user = request.user.id
    attractions_search = list(Attractions.objects.values_list("a_name", flat=True))
    attractions_search_json = json.dumps(attractions_search)
    print(request.GET)
    if request.method == "GET" and request.GET.get("search_text") != None:
        # 初始化一个Q对象，表示没有过滤条件
        filter_condition_and = Q()
        filter_condition_or = Q()
        session_storage = request.GET.getlist('sessionStorage[]', []) 

        data_type = request.GET.get("data_type")
        while len(session_storage) > 0:
            data_type = session_storage.pop()
            search_text = session_storage.pop()
            print(search_text, data_type)
            filter_condition_and, filter_condition_or = keyword_search(
                search_text, filter_condition_and, filter_condition_or, data_type
            )
        print(filter_condition_and)
        search_list_and = list(
            Attractions.objects.filter(filter_condition_and)[:30].values()
        )
        search_list_or = list(
            Attractions.objects.filter(filter_condition_or)
            .exclude(filter_condition_and)[:30]
            .values()
        )
        search_list = search_list_and + search_list_or
            # 判斷是否已收藏
        for index, search in enumerate(search_list):
            if Favorite.objects.filter(u_id=user, a_id=search["id"]).exists():
                search_list[index].setdefault("is_favorite", "1")
            else:
                search_list[index].setdefault("is_favorite", "0")

        html = render_to_string(
            template_name="attraction_details_search.html",
            context={"search_list": search_list},
        )
        data_dict = {"keyword_search_list": html}

        return JsonResponse(data=data_dict, safe=False)
    else:  # 後續要改(目前為顯示前3筆
        keyword_attrations_id = [1, 2, 3]
        for a_id in keyword_attrations_id:
            search_list.append(Attractions.objects.filter(id=a_id).values().first())


    search_list = search_list[:10]  # 之後要改 目前避免當掉

    if request.GET.get("a_id") != None:
        choose_a_id = request.GET.get("a_id")  # 提取傳遞的值
        choose_attractions = Attractions.objects.get(id=choose_a_id)
        choose_attractions.hit += 1
        choose_attractions.save()
        choose_attractions_dict = model_to_dict(choose_attractions)
        is_favorite = Favorite.objects.filter(u_id=user, a_id=choose_attractions.id).exists()
        detail_html = render_to_string(
            template_name="attraction_details_detail.html",
            context={"detail": choose_attractions_dict},
        )
        detail_data_dict = {"attractions_detail_html": detail_html}
        return JsonResponse(data=detail_data_dict, safe=False)

    search_list = is_favorite_list(user, search_list)
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


    # 判斷search_list中是否已收藏的景點
def is_favorite_list(user, search_list):
    for index, search in enumerate(search_list):
        if Favorite.objects.filter(u_id=user, a_id=search["id"]).exists():
            search_list[index].setdefault("is_favorite", "1")
        else:
            search_list[index].setdefault("is_favorite", "0")
    return search_list