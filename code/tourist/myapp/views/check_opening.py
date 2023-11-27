from myapp.models import *


# ------------------------------------確定營業時間(推薦時)
def check_opening(now_time, week, stay_time):
    ok_a_list = []
    now_time += stay_time
    for a in Crowd_Opening.objects.filter(week=week):
        if "休息" not in a.opening:
            if "24小時營業" in a.opening:
                ok_a_list.append(a.a_id)
            else:
                for opening in a.opening:
                    opening = opening.replace(" ", "")
                    if now_time >= int(opening[0:2]) * 60 + int(opening[3:5]) and now_time <= int(opening[6:8]) * 60 + int(opening[9:]):
                        ok_a_list.append(a.a_id)
                        break
                    elif opening[6:8] == "00" and now_time >= int(opening[0:2]) * 60 + int(opening[3:5]) and now_time <= 1440 + int(opening[9:]):
                        ok_a_list.append(a.a_id)
                        break
    return ok_a_list
