from django.shortcuts import render
from myapp.models import *
from .findpicture import get_picture_list
def index(request):
    # 抓熱門資料
    hot_result = Attractions.objects.order_by('hit').values()[:9]
    # hot =[57,79,100,199,216,421,450,454,713]
    # hot_result = Attractions.objects.filter(id__in=hot_result).values()
    user = request.user.id

    for index,attractions in enumerate(hot_result):
        hot_result[index].setdefault("imglist", get_picture_list(attractions["place_id"]))
        if Favorite.objects.filter(u_id=user, a_id=attractions["id"]).exists():
            hot_result[index].setdefault("is_favorite", "1")
        else:
            hot_result[index].setdefault("is_favorite", "0")
    # 讓資料3個一組
    temp_hot=[]
    hotAttractionsList=[]
    for i in hot_result:
        temp_hot.append(i)
        if len(temp_hot)==3:
            hotAttractionsList.append(temp_hot)
            temp_hot=[]
    if len(temp_hot) !=0:
        hotAttractionsList.append(temp_hot)
        temp_hot=[]

    print(hotAttractionsList)
    
    # hot =[57,79,100,199,216,421,450,454,713]
    # for a o in hot:
    #     aDb = Attractions.objects.get()

    # 抓熱門行程
    hot_travel = Create_Travel.objects.filter(status=1).order_by('-like').values()
    top_hot_travel = hot_travel[:3]  # 抓前3名
    #加入place_id
    for index,item in enumerate(top_hot_travel):
        # 放入景點照片
        top_hot_travel[index].setdefault("imglist",list(Create_Travel.get_attractions_picture(item["id"])))
        # 判斷此user有沒有收藏過
        if TravelFavorite.objects.filter(u_id=user, ct_id=item["id"]).exists():
            item['is_favorite']= "1"
        else:
            item['is_favorite']= "0"
        item['u_id'] = User.objects.get(id=item['u_id']) 
    # print(top_hot_travel)
        # #抓user資料庫
    
        # try:
        # # 抓place_id
        #     choiceid= ChoiceDay_Ct.objects.filter(ct_id=item['id']).values().first()
        #     ctaid = Attractions_Ct.objects.filter(choice_ct_id=choiceid['id']).values().first()
        #     print('ctaid',ctaid)
        #     place_id = Attractions.objects.get(id=ctaid['a_id']).place_id
        #     item['img']=place_id
        # except:
        #     item['img']="default"

    return render(request, "index.html", locals())
