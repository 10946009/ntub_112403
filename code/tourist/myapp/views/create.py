from django.shortcuts import render
from datetime import datetime
from myapp.models import *
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .viewsConst import ATT_TYPE_CHINESE
from .recommend import recommend
from .recommend_near import recommend_near
from .final_order import final_order

# 建立行程
@login_required(login_url="/login")
def create(request, ct_id):
    user_favorite = [4, 6, 9, 10, 15, 16, 18]
    ct_data = Create_Travel.objects.get(id=ct_id)
    choiceday = 1
    try:
        ct_attractions_data = ChoiceDay_Ct.objects.get(ct_id=ct_id, day=choiceday)
        ct_attractions_list = Attractions_Ct.objects.filter(
            choice_ct_id=ct_attractions_data.id
        ).values()
    except:
        ct_attractions_list = []
    print(ct_attractions_list)
    travelday = range(1, ct_data.travel_day + 1)
    name = ct_data.ct_name
    start_day = ct_data.start_day
    week = (
        datetime(int(start_day[0:4]), int(start_day[5:7]), int(start_day[8:])).weekday()
        + 1
    )
    ct_id = ct_data.id

    stay_time = 150
    if request.method == "POST":
        ct_status = request.POST["ct_status"]
        print(ct_status)
        if ct_status == "0":
            get_user_address = list(map(float, request.POST["location"].split(",")))
            nowtime = list(map(int, request.POST["nowtime"].split(":")))
            new_nowtime = nowtime[0] * 60 + nowtime[1]
            # nowtime = int(nowtime[:1])*60 + int(nowtime[3:])
            print(get_user_address)
            print(new_nowtime)

            m = recommend(
                user_favorite, new_nowtime, get_user_address, start_day, stay_time
            )
            m_list = Attractions.objects.filter(place_id__in=m)
            crow_opening_list = []
            for i in m_list:
                m_db = (
                    Crowd_Opening.objects.filter(Q(week=week) & Q(a_id=i.id))
                    .values()
                    .first()
                )
                crow_opening_list.append(m_db)
            m_list = list(m_list.values())
            print(m_list)
            print(crow_opening_list[0])
            return JsonResponse(
                {"m_list": m_list, "crow_opening_list": crow_opening_list}
            )

        if ct_status == "1":
            o_attractions_list = request.POST.getlist("select_aid_list[]")
            print(o_attractions_list)
            nowtime = list(map(int, request.POST["nowtime"].split(":")))
            new_nowtime = nowtime[0] * 60 + nowtime[1]
            o = recommend_near(o_attractions_list, new_nowtime, week, stay_time)
            o_list = Attractions.objects.filter(place_id__in=o)
            o_crow_opening_list = []
            for i in o_list:
                o_db = (
                    Crowd_Opening.objects.filter(Q(week=week) & Q(a_id=i.id))
                    .values()
                    .first()
                )
                o_crow_opening_list.append(o_db)
            o_list = list(o_list.values())
            print(o_list)
            print(o_crow_opening_list[0])
            return JsonResponse(
                {"o_list": o_list, "o_crow_opening_list": o_crow_opening_list}
            )

        if ct_status == "2":
            o_attractions_list = request.POST.getlist("all_select[]")
            print(o_attractions_list)
            nowtime = list(map(int, request.POST["nowtime"].split(":")))
            new_nowtime = nowtime[0] * 60 + nowtime[1]
            final = final_order(
                o_attractions_list, new_nowtime, week, stay_time, user_favorite
            )
            # print('final,我在這!!!!!!!!!!!!!!!!',final)
            # ------主要的
            final_result_list = []
            final_crow_opening_list = []
            for f in final[0]:
                temp = Attractions.objects.filter(place_id=f).values().first()
                final_result_list.append(temp)
            for i in final_result_list:
                f_db = (
                    Crowd_Opening.objects.filter(Q(week=week) & Q(a_id=i["id"]))
                    .values()
                    .first()
                )
                final_crow_opening_list.append(f_db)
            # final_result_list = list(final_result_list)
            # ------剩餘的
            final_remainder_result_list = []
            final_remainder_crow_opening_list = []
            try:
                for fr in final[1]:
                    temp_r = Attractions.objects.filter(place_id=fr).values().first()
                    final_remainder_result_list.append(temp_r)

                for i in final_remainder_result_list:
                    fr_db = (
                        Crowd_Opening.objects.filter(Q(week=week) & Q(a_id=i["id"]))
                        .values()
                        .first()
                    )
                    final_remainder_crow_opening_list.append(fr_db)
                # final_remainder_result_list = list(final_remainder_result_list)
            except:
                pass
            # ------------
            print("final_result_list", final_result_list)
            print("final_crow_opening_list", final_crow_opening_list)
            print("final_remainder_result_list", final_remainder_result_list)
            print(
                "final_remainder_crow_opening_list", final_remainder_crow_opening_list
            )

            return JsonResponse(
                {
                    "final_result_list": final_result_list,
                    "final_crow_opening_list": final_crow_opening_list,
                    "final_remainder_result_list": final_remainder_result_list,
                    "final_remainder_crow_opening_list": final_remainder_crow_opening_list,
                }
            )
        choice_ct_id = -1
        if ct_status == "3":
            print("我進來了")
            get_user_address = list(map(float, request.POST["location"].split(",")))
            nowtime = list(map(int, request.POST["nowtime"].split(":")))
            new_nowtime = nowtime[0] * 60 + nowtime[1]
            unit_query = ChoiceDay_Ct.objects.filter(day=choiceday, ct_id=ct_id)
            if unit_query.exists():
                unit = unit_query.first()
                unit.start_location_x = get_user_address[0]
                unit.start_location_y = get_user_address[1]
                unit.start_time = new_nowtime
            else:
                unit = ChoiceDay_Ct.objects.create(
                    day=choiceday,
                    start_location_x=get_user_address[0],
                    start_location_y=get_user_address[1],
                    start_time=new_nowtime,
                    ct_id=ct_id,
                )
            unit.save()
            choice_ct_id = unit.id
            if request.POST["all_id"] != "":
                all_id = list(map(int, request.POST["all_id"].split(",")))
                for index, id in enumerate(all_id):
                    if index == len(all_id) - 1:
                        distance = 0
                        duration = 0
                    else:
                        id_db = Attractions.objects.get(id=id)
                        id2_db = Attractions.objects.get(id=all_id[index + 1])
                        distance = 2200  # 距離(公尺)
                        duration = 10  # 時間(分鐘)
                        # client = googlemaps.Client(key=GOOGLE_PLACES_API_KEY)
                        # response = client.distance_matrix(
                        #     origins=(id_db.location_x,id_db.location_y), #使用者位置
                        #     destinations = (id2_db.location_x,id2_db.location_y), #目的地
                        #     mode="driving", #開車
                        #     units="metric", #公里
                        #     avoid="highways", #限制沒有高速公路
                        #     language="zh-TW",
                        # )
                        # distance = response["rows"][0]["elements"][0]["distance"]["value"]
                        # duration = response["rows"][0]["elements"][0]["duration"]["value"]//60
                    staytime = id_db.stay_time
                    ct = Attractions_Ct.objects.create(
                        a_start_time=new_nowtime,
                        stay_time=staytime,
                        distance=distance,
                        distance_time=duration,
                        order=index + 1,
                        a_id=id,
                        choice_ct_id=choice_ct_id,
                    )
                    ct.save()
                    new_nowtime += 150

            print("hello")

    return render(request, "create.html", locals())