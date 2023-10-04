from django.shortcuts import render
from myapp.models import *
def index(request):
    # 抓熱門資料
    # hot_result = Attractions.objects.order_by('rating', 'rating_total').values()[:9]
    hot =[57,79,100,199,216,421,450,454,713]
    hot_result = Attractions.objects.filter(id__in=hot).values()
    user = request.user.id

    for index,attractions in enumerate(hot_result):
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
    return render(request, "index.html", locals())
