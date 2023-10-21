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

def get_nearby_attractions(choose_attractions):
    for radius in range(1, 10):
            radius = radius / 1000

            min_x = choose_attractions.location_x - radius
            max_x = choose_attractions.location_x + radius
            min_y = choose_attractions.location_y - radius
            max_y = choose_attractions.location_y + radius

            near_attractions = Attractions.objects.filter(
                Q(location_x__range=(min_x, max_x))
                & Q(location_y__range=(min_y, max_y))
                & ~Q(id=choose_attractions.id)
            )[:2].values()
            near_attractions = list(near_attractions)
            if len(near_attractions) == 2:
                break
    return near_attractions

def attraction_details(request, from_base_search_text=None):
    # # 取得景點名稱
    # all_type_name = list(ATT_TYPE_CHINESE.keys())
    all_type_name_json = json.dumps(ATT_TYPE_CHINESE)

    
    # 取得搜尋到的結果
    search_list = []
    if request.user.id:
        user = User.objects.get(id=request.user.id)
    else:
        user = None

    attractions_search = list(Attractions.objects.values_list("a_name", flat=True))
    attractions_search_json = json.dumps(attractions_search)
    # print(request.GET)
    if request.method == "GET" and request.GET.get("search_text") != None:
        # 初始化一个Q对象，表示没有过滤条件
        filter_condition_and = Q()
        filter_condition_or = Q()
        session_storage = request.GET.getlist("sessionStorage[]", [])

        data_type = request.GET.get("data_type")
        while len(session_storage) > 0:
            data_type = session_storage.pop()
            search_text = session_storage.pop()

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
        # 判斷是否已收藏
        for index, search in enumerate(search_list):
            if user and Favorite.objects.filter(u_id=user.id, a_id=search["id"]).exists():
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
        print(choose_attractions)
        choose_attractions.hit += 1
        choose_attractions.save()
        choose_attractions_dict = model_to_dict(choose_attractions)
        # 判斷是否已收藏
        
        is_favorite = Favorite.objects.filter(
            u_id=user.id, a_id=choose_attractions.id
        ).exists() if user  else False
        # 取得擁擠資訊
        crowd = (
            Crowd_Opening.objects.filter(a_id=choose_attractions.id)
            .order_by("week")
            .values()
        )
        crowd_list = list(crowd)
        crowd_dict = [{"week": x["week"], "crowd": x["crowd"]} for x in crowd_list]
        crowd_dict = json.dumps(crowd_dict)
        chinese_week = ["", "一", "二", "三", "四", "五", "六", "日"]
        opentime_list = [
            {"week": chinese_week[int(x["week"])], "opening": x["opening"]}
            for x in crowd_list
        ]
        # 取得照片列表
        picture_list = get_picture_list(choose_attractions.place_id)

        # 取得附近景點
        near_attractions = get_nearby_attractions(choose_attractions)
        

        # 轉HTML格式
        detail_html = render_to_string(
            template_name="attraction_details_detail.html",
            context={
                "detail": choose_attractions_dict,
                "crowd": crowd_dict,
                "picture_list": picture_list,
                "opentime_list": opentime_list,
                "near_attractions":near_attractions,
            },
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
    # print(search_list)
    return render(request, "attraction_details.html", locals())

    # 判斷search_list中是否已收藏的景點


def is_favorite_list(userobject, search_list):
    for index, search in enumerate(search_list):
        if userobject and Favorite.objects.filter(u_id=userobject.id, a_id=search["id"]).exists():
            search_list[index].setdefault("is_favorite", "1")
        else:
            search_list[index].setdefault("is_favorite", "0")
    return search_list


def attraction_details_search(request):
    from_base_search_text = request.POST.get("search_text")
    return attraction_details(request, from_base_search_text)
