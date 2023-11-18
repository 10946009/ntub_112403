import json
from django.shortcuts import render
from myapp.models import *
from django.http import JsonResponse
from django.db.models import Q
from django.template.loader import render_to_string  # 頁面轉成html
from django.forms.models import model_to_dict
from .viewsConst import ATT_TYPE_CHINESE
from .findpicture import get_picture_list
import random

def keyword_search(search_text, filter_condition_and, filter_condition_or, method):
    # Q物件可以用&和|來串接，串接後的Q物件可以用來過濾資料
    if method == "order": return filter_condition_and, filter_condition_or
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
    near_count = 3
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
            )[:near_count].values()
            near_attractions = list(near_attractions)
            if len(near_attractions) == near_count:
                break
    return near_attractions

def attraction_details(request):
    print(request.GET)
    # # 取得景點名稱
    # all_type_name = list(ATT_TYPE_CHINESE.keys())
    loadingpage = 1
    limit = 5
    if request.GET.get("loadingpage"):
        print("loadingpage", request.GET.get("loadingpage"))
        loadingpage = int(request.GET.get("loadingpage"))
    maxlimit = limit*loadingpage
    all_type_name_json = json.dumps(ATT_TYPE_CHINESE)
    if request.POST.get("base_search_text"):
        base_search_text = request.POST.get("base_search_text")
    # 取得搜尋到的結果
    search_list = []
    if request.user.id:
        user = User.objects.get(id=request.user.id)
    else:
        user = None


    # 搜尋引擎
    if request.method == "GET" and request.GET.get("sessionStorage[]") or request.GET.get("data_type") or request.GET.get("order"):
        # 初始化一个Q对象，表示没有过滤条件
        filter_condition_and = Q()
        filter_condition_or = Q()
        session_storage = request.GET.getlist("sessionStorage[]", [])
        order = ""
        while len(session_storage) > 0:
            data_type = session_storage.pop()
            search_text = session_storage.pop()
            if data_type == "order": 
                order = search_text 
                continue

            filter_condition_and, filter_condition_or = keyword_search(
                search_text, filter_condition_and, filter_condition_or, data_type
            )
        search_list_and = list(
            Attractions.objects.filter(filter_condition_and).values()
        )
        search_list_or = list(
            Attractions.objects.filter(filter_condition_or)
            .exclude(filter_condition_and)
            .values()
        )
        search_list = search_list_and + search_list_or if filter_condition_and else search_list_and

        #排序
        if order:
            if order == "favorite":
                for index, search in enumerate(search_list):
                    search_list[index].setdefault("favorite_count",Attractions.objects.get(id=search["id"]).get_favorite_count())
                search_list = sorted(search_list, key=lambda x: x['favorite_count'], reverse=True)
                
            elif order == "hit":
                search_list = sorted(search_list, key=lambda x: x['hit'], reverse=True)
        # 判斷是否已收藏
        for index, search in enumerate(search_list):
            if user and Favorite.objects.filter(u_id=user.id, a_id=search["id"]).exists():
                search_list[index].setdefault("is_favorite", "1")
            else:
                search_list[index].setdefault("is_favorite", "0")

        # print(search_list)
        if search_list:
            html = render_to_string(
                template_name="attraction_details_search.html",
                context={"search_list": search_list[maxlimit-limit:maxlimit]},
            )
            data_dict = {"keyword_search_list": html,
                        "search_list_count" : len(search_list),
                        }
        else:
            data_dict = {"keyword_search_list": "",}

        return JsonResponse(data=data_dict, safe=False)
    else:
        search_list_count = Attractions.objects.all().count()
        search_list = list(Attractions.objects.all().values())[maxlimit-limit:maxlimit]
        search_list = is_favorite_list(user, search_list)
     
    if request.GET.get("loadingpage") and loadingpage != 1:
        if search_list:
            html = render_to_string(
                template_name="attraction_details_search.html",
                context={"search_list": search_list},
            )
            data_dict = {"keyword_search_list": html,}
        else:
            data_dict = {"keyword_search_list": "",}
        return JsonResponse(data=data_dict, safe=False)

    #點擊景點
    if request.GET.get("a_id") != None:
        choose_a_id = request.GET.get("a_id")  # 提取傳遞的值
        choose_attractions = Attractions.objects.get(id=choose_a_id)
        print(choose_attractions)
        choose_attractions.hit += 1
        choose_attractions.save()

        # 記錄使用者點擊
        user_click(user,choose_attractions.id)

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
        
        # 幫停留時間設亂數 為20-60之間間隔為10的任一個數
        if choose_attractions.stay_time == 0:
            choose_attractions.stay_time = random.randrange(20, 70, 10)

        # 取得留言
        comment_list = AttractionsComment.objects.filter(a_id=choose_a_id)
        question_list = AttractionsQuestion.objects.filter(a_id=choose_a_id)
        print('comment_list',comment_list)
        # 轉HTML格式
        detail_html = render_to_string(
            template_name="attraction_details_detail.html",
            context={
                "detail": choose_attractions,
                "crowd": crowd_dict,
                "picture_list": picture_list,
                "opentime_list": opentime_list,
                "near_attractions":near_attractions,
                "request": request,
                "is_favorite":is_favorite,
                "comment_list":comment_list,
                "question_list":question_list,
            },
        )
        detail_data_dict = {"attractions_detail_html": detail_html}
        return JsonResponse(data=detail_data_dict, safe=False)
    
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

def click_info(request):
    #點擊景點
    user = request.user.id
    if request.GET.get("a_id") != None:
        choose_a_id = request.GET.get("a_id")  # 提取傳遞的值
        choose_attractions = Attractions.objects.get(id=choose_a_id)
        print(choose_attractions)
        choose_attractions.hit += 1
        choose_attractions.save()

        user_click(user,choose_attractions.id)

        # 判斷是否已收藏
        
        is_favorite = Favorite.objects.filter(
            u_id=user, a_id=choose_attractions.id
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
        
        # 幫停留時間設亂數 為20-60之間間隔為10的任一個數
        if choose_attractions.stay_time == 0:
            choose_attractions.stay_time = random.randrange(20, 70, 10)

        # 取得留言
        comment_list = AttractionsComment.objects.filter(a_id=choose_a_id)
        question_list = AttractionsQuestion.objects.filter(a_id=choose_a_id)
        print('comment_list',comment_list)
        # 轉HTML格式
        detail_html = render_to_string(
            template_name="attractions_info.html",
            context={
                "detail": choose_attractions,
                "crowd": crowd_dict,
                "picture_list": picture_list,
                "opentime_list": opentime_list,
                "near_attractions":near_attractions,
                "request": request,
                "is_favorite":is_favorite,
                "comment_list":comment_list,
                "question_list":question_list,
            },
        )
        detail_data_dict = {"attractions_detail_html": detail_html}
        return JsonResponse(data=detail_data_dict, safe=False)
    
# 記錄使用者點擊
def user_click(user,aid):
    if user :
        if UserClick.objects.filter(u_id=user.id, a_id=aid).exists():
            user_click = UserClick.objects.get(u_id=user.id, a_id=aid)
            user_click.click_count += 1
            user_click.save()
        else:
            UserClick.objects.create(u_id=user.id, a_id=aid)

        if not user.edit_tag_status :
            user_maybe_list = UserClick.objects.filter(u_id=user.id).order_by('-click_count').values_list('a__att_type', flat=True)[:5]
            user_maybe = [item for x in user_maybe_list for item in x] #拆list
            user_maybe_set = list(set(user_maybe)) #去重複
            user.user_favorite_tag =user_maybe_set
            user.save()
    