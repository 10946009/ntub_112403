from django.db import models
from django.contrib.postgres.fields import ArrayField
# # Create your models here.
# class Comment(models.Model):
#     content = models.TextField(max_length=500)

#     # FK 刪除的策略
#     # models.CASCADE：連帶刪除 -> 刪除 Post 時一併刪除 Comment
#     # models.PROTECT：保護 -> 刪除 Post 時，若有 Comemnt 存在阻止 Post 刪除
#     # models.SET_DEFAULT：刪除 Post 時，將 Comment 中的 post 欄位設定成預設值
#     # models.SET_NULL：刪除 Post 時，將 Comment 中的 post 欄位設定成 null    
#     post = models.ForeignKey(to=Post, on_delete=models.CASCADE)

class User(models.Model):
    name = models.TextField(max_length=500,null=False, blank=False)
    mail = models.TextField(max_length=500,null=False, blank=False)
    gender = models.TextField(max_length=3,null=False, blank=False)
    birthday = models.TextField(max_length=10,null=False, blank=False)

class User_account(models.Model):
    u = models.ForeignKey(to=User, on_delete=models.CASCADE)#user沒了建立行程也會被刪除

    account = models.TextField(max_length=500,null=False, blank=False)
    passwd = models.TextField(max_length=500,null=False, blank=False)
    datetime = models.TimeField(auto_now_add=True)
    is_superuser = models.BooleanField()



class Attractions(models.Model):
    place= models.TextField(max_length=500,null=False, blank=False)
    photo = models.TextField(max_length=500,null=False, blank=False)
    a_name = models.TextField(max_length=500,null=False, blank=False)
    address = models.TextField(max_length=500,null=False, blank=False)
    location_x = models.FloatField()
    location_y = models.FloatField()
    phone = models.TextField(max_length=500,null=False, blank=True)
    opening = ArrayField(models.TextField(), blank=True)
    tags = ArrayField(models.TextField(), blank=True)
    crowd = ArrayField(models.FloatField(), blank=True)
    rating = models.FloatField(null=False, blank=False)
    score = models.FloatField(null=False, blank=False)
    Comment = ArrayField(models.IntegerField(), blank=True)
    stay_time = models.IntegerField(null=True, blank=False)

class Create_Travel(models.Model):
    u = models.ForeignKey(to=User, on_delete=models.CASCADE)#user沒了建立行程也會被刪除

    ct_name = models.IntegerField(null=False, blank=False)
    distance = ArrayField(models.FloatField())
    distance_time = ArrayField(models.IntegerField())
    start_time = models.TimeField()
    end_time = models.TimeField()
    days = models.IntegerField(null=False, blank=False)
    attractions_list = ArrayField(models.IntegerField())

class History(models.Model):
    ct = models.ForeignKey(to=Create_Travel, on_delete=models.CASCADE)#行程沒了歷史也會被刪除
    status = models.BooleanField()


class Share(models.Model):
    h = models.ForeignKey(to=History, on_delete=models.CASCADE)#歷史沒了分享也會被刪除
    like = models.IntegerField(null=False, blank=False)
class Comment(models.Model):
    u = models.ForeignKey(to=User, on_delete=models.CASCADE)#user沒了留言也會被刪除
    a = models.ForeignKey(to=Attractions, on_delete=models.CASCADE)#景點沒了留言也會被刪除
    ct = models.ForeignKey(to=Create_Travel, on_delete=models.CASCADE)#行程沒了留言也會被刪除
    share = models.ForeignKey(to=Share, on_delete=models.CASCADE)#分享沒了留言也會被刪除


    name = models.TextField(max_length=500)
    content = models.TextField(max_length=500)
    score = models.FloatField(null=False, blank=False)
    time = models.TimeField(auto_now_add=True)

class Favorite(models.Model):
    u = models.ForeignKey(to=User, on_delete=models.CASCADE)
    a = models.ForeignKey(to=Attractions, on_delete=models.CASCADE)



class Search(models.Model):
    u = models.ForeignKey(to=User, on_delete=models.CASCADE)
    keyword = ArrayField(models.TextField())