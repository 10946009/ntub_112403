
from myapp.models import *
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# ------------------------------------景點排序(根據使用者喜好、擁擠、營業時間)
def order_check_attractions(
    o_attractions_list, now_time, week, user_favorite
):
    print("now_time", now_time)
    # 判斷當下有沒有營業，沒有就不放進陣列
    ok_a_list = []
    # now_time+=stay_time
    for o in o_attractions_list:
        o_db = Attractions.objects.get(id=o)
        o_crowd_opening = o_db.crowd_opening_set.filter(week=week).values()
        opening = o_crowd_opening[0]["opening"]
        for op in opening:
            if op == "24小時營業":
                ok_a_list.append(o_db.id)
            elif op == "休息":
                continue
            else:
                print(o_db.a_name, now_time, op)
                op = op.replace(" ", "")
                if now_time >= int(op[0:2]) * 60 + int(
                    op[3:5]
                ) and now_time + o_db.stay_time <= int(op[6:8]) * 60 + int(op[9:]):
                    ok_a_list.append(o_db.id)
                    break
                elif str(op[6:8]) == "00" and now_time >= int(op[0:2]) * 60 + int(op[3:5]) and now_time <= 1440 + int(op[9:]):
                    print("ok")
                    ok_a_list.append(o_db.id)
                    break
    if ok_a_list == []:
        return ""
    # 4.將使用者所選擇的所有景點
    #     * 根據使用者提供的資料（喜好）去判斷重複程度（如5個相似，1個相似之類的），沒有的話變成手動給(暫定)，
    o_crowd_list = []
    o_favorite_list = []
    o_opening_list = []
    temp_o_opening_list = []

    for o in ok_a_list:
        score = 0
        o_db = Attractions.objects.get(id=o)
        for tag in o_db.att_type:  # 抓出周遭n的tag(需要修改景點標籤)
            if tag in user_favorite:  #
                score += 1
        o_favorite_list.append(score)

    # 再判斷景點的人潮流量（1-5，1為最高），判斷營業時間
    time = now_time // 60
    # stay_time = 150
    for o in ok_a_list:
        o_db = Attractions.objects.get(id=o)
        o_crowd_opening = o_db.crowd_opening_set.filter(week=week).values()
        crowd = o_crowd_opening[0]["crowd"]
        opening = o_crowd_opening[0]["opening"]
        try:
            crowd = o_crowd_opening[0]["crowd"][time - 1]
            crowd = crowd_judge(crowd)
            o_crowd_list.append(crowd)
        except:
            o_crowd_list.append(0)
        for op in opening:
            # print(op)
            if op == "24小時營業":
                o_opening_list.append(1440)
            else:
                o_opening_list.append(o_db.stay_time)
            break
        # o_opening_list.append(temp_o_opening_list)
        temp_o_opening_list = []
    print("ok_a_list", ok_a_list)
    print("o_opening_list", o_opening_list)

    # print("o_crowd_list:",o_crowd_list)
    # print("o_favorite_list:",o_favorite_list)

    o_list = {
        "o_favorite_list": o_favorite_list,
        "o_crowd_list": o_crowd_list,
        "o_opening_list": o_opening_list,
    }
    df = pd.DataFrame(o_list)
    df["total"] = 0
    print("df", df)
    df_html = df.to_html()
    # 標準化 使值在[0,1]之間
    scaler = MinMaxScaler(feature_range=(0, 1)).fit(df)
    X_scaled = scaler.transform(df)
    df_x = pd.DataFrame(X_scaled)

    df_x[3] = (
        df_x[0].mul(0.2) + df_x[1].mul(0.4) + (1 - df_x[2]).mul(0.4)
    )  # 將值皆乘0.5相加後放入total欄位
    print("df_x", df_x)
    df_x_html = df_x.to_html()
    total_list = df_x[3].values.tolist()  # 將df_x[3]的值轉成list
    final = [
        [ok_a_list[x], total_list[x]] for x in range(len(total_list))
    ]  # 將id和分數合併
    f_final_list = sorted(final, key=lambda x: x[1], reverse=True)  # 排序
    print("f_final_list", f_final_list)
    f_final_list_name = [
        [
            Attractions.objects.get(id=x[0]).id,
            Attractions.objects.get(id=x[0])
            .crowd_opening_set.filter(week=week)
            .values()[0]["opening"],
        ]
        for x in f_final_list
    ]  # name的List
    # print("時間:",opening,",擁擠:",crowd)
    # print("這裡",o_crowd_opening)
    #     * 最後使用normalization將兩者的區間變成[0,1]，再賦予他們權重（如0.5、0.5），最後根據分數去排序景點。
    return f_final_list[0][0]




# 判斷人潮程度
def crowd_judge(crowd):
    if crowd >= 80:
        return 1
    elif crowd >= 60:
        return 2
    elif crowd >= 40:
        return 3
    elif crowd >= 20:
        return 4
    elif crowd > 0:
        return 5
    else:
        return 0