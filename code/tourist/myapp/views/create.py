from django.shortcuts import render
from datetime import datetime

import googlemaps
from myapp.models import *
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .viewsConst import ATT_TYPE_CHINESE
from .recommend import recommend,recommend_maybe,recommend_user_favorite
from .recommend_near import recommend_near
from .final_order import final_order
import requests
from geopy.geocoders import Nominatim
from django.template.loader import render_to_string  # 頁面轉成html
import os
from os.path import join, dirname
from dotenv import load_dotenv, find_dotenv
import json
from .weather import get_weather_data

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path, override=True)  # 設定 override 才會更新變數哦！
GOOGLE_PLACES_API_KEY = os.environ.get("GOOGLE_PLACES_API_KEY")
apikey = GOOGLE_PLACES_API_KEY
def format_minutes_as_time(minutes):
    hours, remainder_minutes = divmod(minutes, 60)
    return f"{hours:02d}:{remainder_minutes:02d}"

# 之後沒用到可以刪掉
# def local_to_address(lat,lng):
#     print("lat",lat)
#     print("lng",lng)
#     base_url = 'https://maps.googleapis.com/maps/api/geocode/json'
#     params = {
#         'latlng': f'{lat},{lng}',
#         'key': apikey,
#         'language': 'zh-TW'  # 设置语言为繁体中文
#     }

#     # 发送请求
#     response = requests.get(base_url, params=params)
#     data = response.json()

#     # 解析结果
#     if data['status'] == 'OK' and len(data['results']) > 0:
#         formatted_address = data['results'][0]['formatted_address']
#         print('地址：', formatted_address)
#     else:
#         formatted_address = "無法獲取地址"
#         print('无法获取地址')
#     return formatted_address

# 建立行程
@login_required(login_url="/login")
def create(request, ct_id):
    # 抓使用者收藏的景點
    uid = request.user.id
    user_favorite_type = request.user.user_favorite_tag #需修改新增的部分
    ct_data = Create_Travel.objects.get(id=ct_id)
    try:
        apikey = GOOGLE_PLACES_API_KEY   #記得一定要打開!!!!!!!!!!!!!!!!!!!!!!!!!(API在這!)
    except:
        apikey = None
    apikey = None
    print("apikey",apikey)
    travelday = range(1, ct_data.travel_day + 1)
    name = ct_data.ct_name
    start_day = ct_data.start_day
    start_week = (datetime(int(start_day[0:4]), int(start_day[5:7]), int(start_day[8:])).weekday()+ 1)
    # print(start_week)
    # ct_id = ct_data.id
    
    stay_time = 150
    ct_attractions_detail_list=[]
    ct_attractions_co_list=[]
    all_ct_data = {} #days從1開始
    all_ct_data_id = {}
    travel_datas = {}
    # 抓出這是哪一筆行程
    ct_attractions_data_total = ChoiceDay_Ct.objects.filter(ct_id=ct_id).order_by('day')
    user_favorite = Favorite.objects.filter(u_id = uid)
    user_favorite_id_list = [uf.a_id for uf in user_favorite]
    # 預設總共天數的資料為""
    for i in range(1,ct_data.travel_day+1):
       travel_datas[i]="" 
    # 抓目前位置
    for index,ct_attractions_data in enumerate(ct_attractions_data_total):
            
        # chinese_week = ["","一","二","三","四","五","六","日"]
        week = (start_week + index) % 8
        if week == 0: week = 1
        user_favorite_list = Crowd_Opening.objects.filter(week=week, a_id__in=user_favorite_id_list)
        crowd_index_list=[]
        ct_data = []
        ct_data_id = []
        ct_attractions_list = []
        ct_attractions_detail_list =[]
        local_xy = [ct_attractions_data.start_location_x,ct_attractions_data.start_location_y] # 抓使用者位置的經緯度
        location_name = ct_attractions_data.location_name # 抓使用者位置的地址或名稱
        user_nowtime = format_minutes_as_time(ct_attractions_data.start_time) # 抓出發時
        # 每一天的基本資料(起始時間、位置等)
        travel_datas[index+1] = {
            "day": index+1,
            "local_xy": local_xy,
            "location_name": location_name,
            "user_nowtime": user_nowtime,
            "date": f"{start_day[5:7]}月{int(start_day[8:])+index}日",
            # "week": chinese_week[week],
            "week": week,
            "user_favorite_list": user_favorite_list,
        }
        # 抓出這筆行程中的所有景點
        ct_attractions_list = Attractions_Ct.objects.filter(
            choice_ct_id=ct_attractions_data.id
        ).order_by('order').values()
    
        # 抓出所有景點的詳細資料
        for a in ct_attractions_list:
            crowd_index_list.append((int(a['a_start_time']//60)%24)) #人潮流量索引
            ct_attractions_detail_list.append(Attractions.objects.get(id=a['a_id']))
            ct_data_id.append(a['a_id'])

        for co in ct_attractions_detail_list:
            ct_attractions_co_list.append(Crowd_Opening.objects.get(a_id=co.id,week=week))

        for attraction, detail, co ,cl  in zip(ct_attractions_list, ct_attractions_detail_list, ct_attractions_co_list,crowd_index_list):
            ct_data.append({
                "attraction": attraction,
                "detail": detail,
                "co": co,
                "crowd_list" : f"{min(co.crowd[cl],co.crowd[(cl+1)%24])} ~ {max(co.crowd[cl],co.crowd[(cl+1)%24])}",
                "crowd_avg": (co.crowd[cl]+co.crowd[(cl+1)%24])//2,
                "weather": get_weather_data(detail.address,start_day[0:4],start_day[5:7],int(start_day[8:])+index,ct_attractions_data.start_time),
            })
            
        all_ct_data[index+1]=ct_data
        all_ct_data_id[index+1]=ct_data_id
        # print('all_ct_data',all_ct_data)
    # except:
    #     all_ct_data=[]

    all_ct_data_id=json.dumps(all_ct_data_id)
    if request.method == "POST":
        ct_status = request.POST["ct_status"]
        #這是推薦景點~
        if ct_status == "0":
            globalDay = int(request.POST["globalDay"])
            week = (start_week + globalDay - 1) % 7
            get_user_address = list(map(float, request.POST["user_location"].split(",")))
            nowtime = list(map(int, request.POST["nowtime"].split(":")))
            new_nowtime = nowtime[0] * 60 + nowtime[1]
            # print("user目前位置",get_user_address)
            # print("user目前位置",type(get_user_address))
            # print(new_nowtime)
            m = recommend(
                user_favorite_type, new_nowtime, get_user_address, start_day, stay_time
            )
            m_list = (Attractions.objects.filter(place_id__in=m) | recommend_maybe(uid)|recommend_user_favorite(uid)).distinct()
            crow_opening_list = []
            for i in m_list:
                m_db = (
                    Crowd_Opening.objects.filter(Q(week=week) & Q(a_id=i.id))
                    .values()
                    .first()
                )
                crow_opening_list.append(m_db)
            # print('m_list',m_list)
            # print('crow_opening_list',crow_opening_list[0])
            recommend_data= []
            for m, fc in zip(m_list, crow_opening_list):
                recommend_data.append({
                    'm_list': m,
                    'crow_opening_list': fc, 
                })

            html = render_to_string(
                template_name="create_recommend.html",
                context={"recommend_data": recommend_data},
            )
            data_dict = {"recommend_attractions_list": html}
            
            return JsonResponse(data=data_dict, safe=False)

        if ct_status == "1":
            globalDay = int(request.POST["globalDay"])
            week = (start_week + globalDay - 1) % 7
            
            o_attractions_list = request.POST.getlist("aid_list[]")
            nowtime = list(map(int, request.POST["nowtime"].split(":")))
            new_nowtime = nowtime[0] * 60 + nowtime[1]
            o = recommend_near(list(map(int,o_attractions_list)), new_nowtime, week, stay_time)
            o_list = Attractions.objects.filter(id__in=o)
            o_crow_opening_list = []
            for i in o_list:
                o_db = (
                    Crowd_Opening.objects.filter(Q(week=week) & Q(a_id=i.id))
                    .values()
                    .first()
                )
                o_crow_opening_list.append(o_db)
            o_list = list(o_list.values())
            # print(o_list)
            # print(o_crow_opening_list[0])
            
            near_recommend_data= []
            for o, oc in zip(o_list, o_crow_opening_list):
                near_recommend_data.append({
                    'o_list': o,
                    'o_crow_opening_list': oc,
                })
            html = render_to_string(
                template_name="create_similar_recommend.html",
                context={"near_recommend_data": near_recommend_data,"nowchoice":o_attractions_list},
            )
            data_dict = {"recommend_attractions_list": html}
            
            return JsonResponse(data=data_dict, safe=False)

        if ct_status == "2":
            globalDay = int(request.POST["globalDay"])
            week = (start_week + globalDay - 1) % 7
            o_attractions_list = request.POST.getlist("total_aid_list[]")
            # print('o_attractions_list我在這!!!!!!!!!!!!!!!!!!',o_attractions_list)
            nowtime = list(map(int, request.POST["nowtime"].split(":")))
            new_nowtime = nowtime[0] * 60 + nowtime[1]
            final = final_order(
                list(map(int,o_attractions_list)), new_nowtime, week, user_favorite_type
            )
            # print('final,我在這!!!!!!!!!!!!!!!!',final)
            # ------主要的
            final_result_list = []
            final_crow_opening_list = []
            for f in final[0]:
                temp = Attractions.objects.filter(id=f).values().first()
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
            for fr in final[1]:
                temp_r = Attractions.objects.filter(id=fr).values().first()
                final_remainder_result_list.append(temp_r)
            for i in final_remainder_result_list:
                print(i)
                fr_db = (
                    Crowd_Opening.objects.filter(Q(week=week) & Q(a_id=i["id"]))
                    .values()
                    .first()
                )
                final_remainder_crow_opening_list.append(fr_db)
            # final_remainder_result_list = list(final_remainder_result_list)

            final_now_time_list = final[2]
            # ------------
            # print("final_result_list", final_result_list)
            # print("final_crow_opening_list", final_crow_opening_list)
            # print("final_remainder_result_list", final_remainder_result_list)
            # print(
            #     "final_remainder_crow_opening_list", final_remainder_crow_opening_list
            # )
            # print('final_now_time_list',final_now_time_list)
            # return JsonResponse(
            #     {
            #         "final_result_list": final_result_list,
            #         "final_crow_opening_list": final_crow_opening_list,
            #         "final_remainder_result_list": final_remainder_result_list,
            #         "final_remainder_crow_opening_list": final_remainder_crow_opening_list,
            #         'final_now_time_list':final_now_time_list,
            #     }
            # )
            # 將資料組在一起
            order_attractions_data= []
            remainder_attractions_data = []
            for fr, fc, fnowtime in zip(final_result_list, final_crow_opening_list,final_now_time_list):
                f_nt = (fnowtime//60)%24
                f_nt_next = (f_nt +1) % 24 
                print(f_nt)
                order_attractions_data.append({
                    'final_result_list': fr,
                    'final_crow_opening_list': fc,
                    'final_crowd_list' : f"{min(fc['crowd'][f_nt],fc['crowd'][f_nt_next])} ~ {max(fc['crowd'][f_nt],fc['crowd'][f_nt_next])}",
                    "final_crowd_avg": (fc['crowd'][f_nt]+fc['crowd'][f_nt_next])//2,  
                    'weather': get_weather_data(fr['address'],start_day[0:4],start_day[5:7],int(start_day[8:])+index,fnowtime),
                })
            for frr,frc in zip(final_remainder_result_list,final_remainder_crow_opening_list):
                remainder_attractions_data.append({
                'final_result_list':frr,
                'final_crow_opening_list':frc,
            })
            #轉成html
            html = render_to_string(
                template_name="create_order_attractions.html",
                context={"order_attractions_data": order_attractions_data,'final_now_time_list':final_now_time_list},
            )
            html2 = render_to_string(
                template_name="create_remainder_attractions.html",
                context={'remainder_attractions_data':remainder_attractions_data},
            )

            data_dict = {"order_attractions": html,"remainder_attractions":html2}
            
            return JsonResponse(data=data_dict, safe=False)

        choice_ct_id = -1
        if ct_status == "3":
            print("我進來了")
            print(request.POST)
            choiceday = int(request.POST["day"])
            print("choiceday",choiceday,"ct_id",ct_id)
            get_user_address = list(map(float, request.POST["location"].split(",")))
            get_user_location_name = request.POST["location_name"]
            nowtime = list(map(int, request.POST["nowtime"].split(":")))
            new_nowtime = nowtime[0] * 60 + nowtime[1]
            unit_query = ChoiceDay_Ct.objects.filter(day=choiceday, ct_id=ct_id)
            print(unit_query)
            if unit_query.exists():
                unit = unit_query.first()
                unit.start_location_x = get_user_address[0]
                unit.start_location_y = get_user_address[1]
                unit.start_time = new_nowtime
                unit.location_name = get_user_location_name
            # else: #已經會自己生成了
            #     unit = ChoiceDay_Ct.objects.create(
            #         day=choiceday,
            #         start_location_x=get_user_address[0],
            #         start_location_y=get_user_address[1],
            #         start_time=new_nowtime,
            #         ct_id=ct_id,
            #         location_name=get_user_location_name,
            #     )
            unit.save()
            choice_ct_id = unit.id
            if request.POST["all_id"] != "":
                print(request.POST["all_id"])
                all_id = list(map(int, request.POST["all_id"].split(",")))
                print("all_id",all_id)
                Attractions_Ct.objects.filter(choice_ct_id=choice_ct_id).delete() #刪除舊資料
                for index, id in enumerate(all_id):
                    id_db = Attractions.objects.get(id=id)
                    if apikey: # 第一個景點
                        client = googlemaps.Client(key=apikey)
                        if index == 0:
                            response = client.distance_matrix(
                                origins=(get_user_address[0],get_user_address[1]), #使用者位置
                                destinations = (id_db.location_x,id_db.location_y), #目的地
                                mode="driving", #開車
                                units="metric", #公里
                                avoid="highways", #限制沒有高速公路
                                language="zh-TW",
                            )
                        else :
                            id2_db = Attractions.objects.get(id=all_id[index-1])
                            response = client.distance_matrix(
                                origins=(id_db.location_x,id_db.location_y), #使用者位置
                                destinations = (id2_db.location_x,id2_db.location_y), #目的地
                                mode="driving", #開車
                                units="metric", #公里
                                avoid="highways", #限制沒有高速公路
                                language="zh-TW",
                            )
                        distance = response["rows"][0]["elements"][0]["distance"]["value"]
                        duration = response["rows"][0]["elements"][0]["duration"]["value"]//60
                    else:
                        distance = 2200  # 距離(公尺)
                        duration = 10  # 時間(分鐘)
                        print(index,distance,duration)
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
                    new_nowtime += duration + staytime
            else:
                Attractions_Ct.objects.filter(choice_ct_id=choice_ct_id).delete() #為空就刪除資料

    return render(request, "create.html", locals())