
from myapp.models import *
from .viewsConst import ATT_TYPE_LIST
from .check_opening import check_opening
from .check_distance import check_distance_id
# ------------------------------------第2步驟(推薦相似景點)
def recommend_near(o_attractions_list, now_time, week, stay_time,ispet):
    # 2.選擇一些景點做為O（使用者選擇的景點）
    # 抓取使用者所選的景點ID

    # o_attractions_list_name = [
    #     "華山1914文化創意產業園區",
    #     "URS27-華山大草原",
    # ]
    near_o = []
    # 相似標籤

    # 抓o周遭的景點
    for o in o_attractions_list:
        o_db = Attractions.objects.get(id=o)
        o_x = o_db.location_x
        o_y = o_db.location_y
        near_o += check_distance_id(
            (o_x, o_y), check_opening(now_time, week, stay_time),ispet
        )

    # 去掉o_attractions_list本身
    near_o = list(set(near_o) - set(o_attractions_list))
    print("先前所選的景點為", o_attractions_list)
    print("周遭的景點為", near_o)
    # 3.根據O裡面的景點，利用tag找出相似景點並推薦（組成新的O)
    tags_same_score = []
    tags_same_score_total = []
    p_attractions_list = []
    # -----------------根據type，推薦相似的景點
    for n in near_o:
        n_db = Attractions.objects.get(id=n)
        for o in o_attractions_list:
            score = 0
            o_db = Attractions.objects.get(id=o)
            # 新增相似標籤------------------!!!!!!
            for tag in n_db.att_type:  # 抓出周遭n的tag(需要修改景點標籤)
                if tag in o_db.att_type:  #
                    score += 1
            tags_same_score.append(score)
        tags_same_score_total.append(tags_same_score)
        tags_same_score = []
    # print("tags_same_score_total:",tags_same_score_total)
    max_i_list = []
    f_max_i_list = []
    for index, i in enumerate(tags_same_score_total):
        max_i_list.append([index, max(i)])
    # print("max_i_list:",max_i_list)
    f_max_i_list = sorted(max_i_list, key=lambda x: x[1], reverse=True)[0:10]
    # print("f_max_i_list:",f_max_i_list)
    if len(near_o) < 10:
        for i in range(len(near_o)):
            p_attractions_list.append(near_o[f_max_i_list[i][0]])
    else:
        for i in range(10):
            p_attractions_list.append(near_o[f_max_i_list[i][0]])
    near_o = list(set(near_o) - set(p_attractions_list))
    # --------------根據組合，推薦類似type的景點
    o_type = []  # 宣告相似組合的陣列
    tags_same_score_total = []
    for o in o_attractions_list:
        o_db = Attractions.objects.get(id=o)
        for a_tag in o_db.att_type:
            for i in ATT_TYPE_LIST:
                if a_tag == i[0]:
                    for x in i:
                        o_type.append(x)
    o_type = list(set(o_type))
    for n in near_o:
        n_db = Attractions.objects.get(id=n)
        score = 0
        for tag in n_db.att_type:  # 抓出周遭n的tag(需要修改景點標籤)
            if tag in o_type:  #
                score += 1
        tags_same_score_total.append(score)
    print("tags_same_score_total:", tags_same_score_total)
    max_i_list = []
    f_max_i_list = []
    for index, i in enumerate(tags_same_score_total):
        max_i_list.append([index, i])
    # print("max_i_list:",max_i_list)
    f_max_i_list = sorted(max_i_list, key=lambda x: x[1], reverse=True)[0:10]
    # print("f_max_i_list:",f_max_i_list)
    if len(near_o) < 10:
        for i in range(len(near_o)):
            p_attractions_list.append(near_o[f_max_i_list[i][0]])
    else:
        for i in range(10):
            p_attractions_list.append(near_o[f_max_i_list[i][0]])
    print("推薦相似景點的順序:", p_attractions_list)
    p_attractions_list = [
        Attractions.objects.get(id=x).id for x in p_attractions_list
    ]  # name的List
    return p_attractions_list
