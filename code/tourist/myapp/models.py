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
    account = models.TextField(max_length=500,null=False, blank=False)
    passwd = models.TextField(max_length=500,null=False, blank=False)
    datetime = models.TimeField(auto_now_add=True)
    is_superuser = models.BooleanField(default=0,null=False)
    name = models.TextField(max_length=500,null=False, blank=False)
    mail = models.TextField(max_length=500,null=False, blank=False)
    gender = models.TextField(max_length=3,null=False, blank=False)
    birthday = models.TextField(max_length=10,null=False, blank=False)
    user_photo = models.TextField(max_length=10,null=False, blank=False,default="")
    
class Attractions(models.Model):
    place_id= models.TextField(max_length=500, blank=False)
    photo = models.TextField(max_length=500,null=False, blank=False,default="")
    a_name = models.TextField(max_length=500,null=False, blank=False)
    address = models.TextField(max_length=500,null=False, blank=False)
    location_x = models.FloatField()
    location_y = models.FloatField()
    phone = models.TextField(max_length=500,null=False, blank=True)
    rating = models.FloatField(null=False, blank=False)
    score = models.FloatField(default=0,null=False, blank=False)
    stay_time = models.IntegerField(null=True, blank=False)
    hot_month = ArrayField(models.IntegerField())
    att_type = models.IntegerField(null=False, blank=False)


class Crowd_Opening(models.Model):
    a = models.ForeignKey(to=Attractions, on_delete=models.SET_DEFAULT,default=-1)#景點沒了留言a_id會被設為null
    weak =  models.IntegerField(null=False, blank=False)
    crowd = ArrayField(models.IntegerField())
    opening = models.TextField(max_length=500,default="")

    
class Create_Travel(models.Model):
    u = models.ForeignKey(to=User, on_delete=models.CASCADE)#user沒了建立行程也會被刪除
    ct_name = models.IntegerField(null=False, blank=False)
    start_location_x = models.FloatField(null=False, blank=False)
    start_location_y = models.FloatField(null=False, blank=False)
    start_day = models.TextField(max_length=500,null=False, blank=False)
    end_day = models.TextField(max_length=500,null=False, blank=False)
    days = models.IntegerField(null=False, blank=False)
    start_time = models.IntegerField(null=False, blank=False)

    
class Attractions_Ct(models.Model):
    ct = models.ForeignKey(to=Create_Travel, on_delete=models.SET_DEFAULT,default=-1)#行程沒了歷史也會被刪除
    a = models.ForeignKey(to=Attractions, on_delete=models.SET_DEFAULT,default=-1)#景點沒了留言a_id會被設為null
    choice_day = models.IntegerField(null=False,blank=False, default=1)
    a_time = models.IntegerField(null=False,blank=False)
    stay_time = models.IntegerField(null=False,blank=False)
    distance = models.FloatField(null=False, blank=False)
    distance_time =models.IntegerField(null=False,blank=False)
    order = models.IntegerField(null=False,blank=False)
  
class History(models.Model):
    ct = models.ForeignKey(to=Create_Travel, on_delete=models.SET_DEFAULT,default=-1)#行程沒了歷史也會被刪除
    status = models.BooleanField()
    like = models.IntegerField(default=0,null=True, blank=True)


class Comment(models.Model):
    u = models.ForeignKey(to=User, on_delete=models.SET_DEFAULT,default=-1)#user沒了留言u_id會被設為null
    a = models.ForeignKey(to=Attractions, on_delete=models.SET_DEFAULT,default=-1)#景點沒了留言a_id會被設為null
    h = models.ForeignKey(to=History, on_delete=models.SET_DEFAULT,default=-1)#分享沒了留言會被設為null
    content = models.TextField(max_length=500)
    score = models.FloatField(null=False, blank=False)
    time = models.TimeField(auto_now_add=True)
    comment_type = models.BooleanField(default=False) #0為行程留言，1為景點留言

class Favorite(models.Model):
    u = models.ForeignKey(to=User, on_delete=models.CASCADE)
    a = models.ForeignKey(to=Attractions, on_delete=models.CASCADE)


class Search(models.Model):
    attractions =  models.ManyToManyField(Attractions)
    IP_address = models.TextField(max_length=500,null=False, blank=False)
    keyword = ArrayField(models.TextField())
    identify = models.BooleanField(default=False) #0為訪客，1為會員