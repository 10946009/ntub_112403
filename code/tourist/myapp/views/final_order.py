from .order_check_attractions import order_check_attractions
from myapp.models import *
# ------------------------------------第3步驟(最後的排序)
def final_order(o_attractions_list, now_time, week, stay_time, user_favorite):
    final_list = []
    remainder_list = []
    all_list = []
    now_time_list = [now_time]
    while len(o_attractions_list) > 0:
        temp = order_check_attractions(
            o_attractions_list, now_time, week, stay_time, user_favorite
        )
        if temp == "":
            break
        final_list.append(temp)
        now_time += stay_time
        now_time_list.append(now_time)
        o_attractions_list = list(set(o_attractions_list) - set(final_list))
    remainder_list = [
        Attractions.objects.get(place_id=x).place_id
        # Attractions.objects.get(place_id=x).crowd_opening_set.filter(week=week).values()[0]["opening"],
        for x in o_attractions_list
    ]
    # f_final_list_name = [
    #     Attractions.objects.get(place_id=x).place_id
    #     # Attractions.objects.get(place_id=x).crowd_opening_set.filter(week=week).values()[0]["opening"],
    #     for x in final_list
    # ]
    print("final_list!!!!!!!!!!!!!", final_list)
    all_list.append(final_list)
    all_list.append(remainder_list)
    all_list.append(now_time_list)
    return all_list
