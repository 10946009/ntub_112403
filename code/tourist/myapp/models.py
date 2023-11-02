from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractUser

# # Create your models here.
# class Comment(models.Model):
#     content = models.TextField(max_length=255)

#     # FK 刪除的策略
#     # models.CASCADE：連帶刪除 -> 刪除 Post 時一併刪除 Comment
#     # models.PROTECT：保護 -> 刪除 Post 時，若有 Comemnt 存在阻止 Post 刪除
#     # models.SET_DEFAULT：刪除 Post 時，將 Comment 中的 post 欄位設定成預設值
#     # models.SET_NULL：刪除 Post 時，將 Comment 中的 post 欄位設定成 null
#     post = models.ForeignKey(to=Post, on_delete=models.CASCADE)


# django內建方法
class User(AbstractUser):
    first_name = None
    last_name = None
    email = models.EmailField(unique=True, max_length=255, blank=False, null=False)
    username = models.CharField(
        verbose_name="username", max_length=255, blank=False, null=False
    )
    gender = models.TextField(max_length=3, null=False, blank=False)
    birthday = models.TextField(max_length=10, null=False, blank=False)
    user_photo = models.TextField(max_length=10, blank=True, default="")
    verification_token = models.TextField(max_length=32, default="")
    USERNAME_FIELD = "email"  # 使用信箱當登入帳號
    REQUIRED_FIELDS = ["username"]  # username 是預設的必填欄位

    class Meta:
        verbose_name = "user"
        verbose_name_plural = verbose_name


# class User(models.Model):
#     account = models.TextField(max_length=255,null=False, blank=False)
#     passwd = models.TextField(max_length=255,null=False, blank=False)
#     datetime = models.TimeField(auto_now_add=True)
#     is_superuser = models.BooleanField(default=0,null=False)
#     name = models.TextField(max_length=255,null=False, blank=False)
#     mail = models.TextField(max_length=255,null=False, blank=False)
#     gender = models.TextField(max_length=3,null=False, blank=False)
#     birthday = models.TextField(max_length=10,null=False, blank=False)
#     user_photo = models.TextField(max_length=10,blank=True,default="")


class Attractions(models.Model):
    place_id = models.TextField(max_length=255, blank=False)
    photo = models.TextField(max_length=255, null=False, blank=False, default="")
    a_name = models.TextField(max_length=255, null=False, blank=False)
    address = models.TextField(max_length=255, null=False, blank=False)
    location_x = models.FloatField()
    location_y = models.FloatField()
    phone = models.TextField(max_length=255, null=False, blank=True)
    rating = models.FloatField(null=False, blank=False)
    rating_total = models.IntegerField(null=False, blank=False, default=-1)
    hit = models.IntegerField(default=0, null=False, blank=False)
    stay_time = models.IntegerField(null=True, blank=False)
    hot_month = ArrayField(models.IntegerField())
    att_type = ArrayField(models.IntegerField())
    detail = models.TextField(max_length=255, null=False, blank=False, default="")
    # def __str__(self):
    #     return f'{self.id} {self.a_name}'


class Crowd_Opening(models.Model):
    a = models.ForeignKey(
        to=Attractions, on_delete=models.SET_DEFAULT, default=-1
    )  # 景點沒了留言a_id會被設為null
    week = models.IntegerField(null=False, blank=False)
    crowd = ArrayField(models.IntegerField())
    opening = ArrayField(models.TextField(max_length=255))


class Create_Travel(models.Model):
    u = models.ForeignKey(to=User, on_delete=models.CASCADE)  # user沒了建立行程也會被刪除
    ct_name = models.TextField(null=False, blank=False)
    start_day = models.TextField(max_length=255, null=False, blank=False)
    create_date = models.DateField(auto_now_add=True)
    travel_day = models.IntegerField(null=False, blank=False, default=1)
    status = models.BooleanField(null=False, blank=False, default=0)
    like = models.IntegerField(default=0, null=False, blank=False)


class ChoiceDay_Ct(models.Model):
    ct = models.ForeignKey(to=Create_Travel, on_delete=models.CASCADE)  # 行程沒了歷史也會被刪除
    day = models.IntegerField(null=False, blank=False)
    location_name = models.TextField(max_length=255, null=False, blank=False,default="臺北")
    start_location_x = models.FloatField(null=False, blank=False)
    start_location_y = models.FloatField(null=False, blank=False)
    start_time = models.IntegerField(null=False, blank=False)


class Attractions_Ct(models.Model):
    choice_ct = models.ForeignKey(
        to=ChoiceDay_Ct, on_delete=models.CASCADE, default=-1
    )  # 行程沒了也會被刪除
    a = models.ForeignKey(
        to=Attractions, on_delete=models.SET_DEFAULT, default=-1
    )  # 景點沒了a_id會被設為-1
    a_start_time = models.IntegerField(null=False, blank=False)
    stay_time = models.IntegerField(null=False, blank=False)
    distance = models.FloatField(null=False, blank=False)
    distance_time = models.IntegerField(null=False, blank=False)
    order = models.IntegerField(null=False, blank=False)


# class History(models.Model):
#     ct = models.ForeignKey(
#         to=Create_Travel, on_delete=models.SET_DEFAULT, default=-1
#     )  # 行程沒了歷史也會被刪除
#     status = models.BooleanField()
#     like = models.IntegerField(default=0, null=True, blank=True)

# 景點問問題和回答問題的資料庫
class AttractionsQuestion(models.Model):
    u = models.ForeignKey(
        to=User, on_delete=models.SET_DEFAULT, default=-1
    )  # user沒了問題u_id會被設為null
    a = models.ForeignKey(
        to=Attractions, on_delete=models.SET_DEFAULT, default=-1
    )  # 景點沒了留言a_id會被設為null
    content = models.TextField(max_length=255,default="")
    question_date = models.DateField(auto_now_add=True, null=False, blank=False)
    def get_answer(self):
        return AttractionsAnswer.objects.filter(aq_id=self.id)
    # @property
    # def name(self):
    #     return self.get_name()
    
class AttractionsAnswer(models.Model):
    u = models.ForeignKey(
        to=User, on_delete=models.SET_DEFAULT, default=-1
    )  # user沒了留言u_id會被設為null
    aq = models.ForeignKey(
        to=AttractionsQuestion, on_delete=models.SET_DEFAULT, default=-1
    )  # 問題沒了aq_id會被設為null
    content = models.TextField(max_length=255,default="")
    answer_date = models.DateField(auto_now_add=True, null=False, blank=False)



class AttractionsComment(models.Model):
    u = models.ForeignKey(
        to=User, on_delete=models.SET_DEFAULT, default=-1
    )  # user沒了留言u_id會被設為null
    a = models.ForeignKey(
        to=Attractions, on_delete=models.SET_DEFAULT, default=-1
    )  # 景點沒了留言a_id會被設為null
    content = models.TextField(max_length=255,default="")
    comment_date = models.DateField(auto_now_add=True, null=False, blank=False)

    # def get_name(self):
    #     return self.u.username
    # @property
    # def name(self):
    #     return self.get_name()

class AttractionsCommentFavorite(models.Model):
    ac = models.ForeignKey(
        to=AttractionsComment, on_delete=models.CASCADE, default=-1
    )  # 景點沒了留言a_id會被設為null
    u = models.ForeignKey(
        to=User, on_delete=models.SET_DEFAULT, default=-1
    )  # user沒了留言u_id會被設為null

    
class TravelComment(models.Model):
    u = models.ForeignKey(
        to=User, on_delete=models.SET_DEFAULT, default=-1
    )  # user沒了留言u_id會被設為null
    ct = models.ForeignKey(to=Create_Travel, on_delete=models.SET_DEFAULT , default=-1)
    content = models.TextField(max_length=255,default="")
    comment_date = models.DateField(auto_now_add=True, null=False, blank=False)

class TravelCommentFavorite(models.Model):
    tc = models.ForeignKey(
        to=TravelComment, on_delete=models.CASCADE, default=-1
    )  # 景點沒了留言a_id會被設為null
    u = models.ForeignKey(
        to=User, on_delete=models.SET_DEFAULT, default=-1
    )  # user沒了留言u_id會被設為null

# 我的最愛
class Favorite(models.Model):
    u = models.ForeignKey(to=User, on_delete=models.CASCADE)
    a = models.ForeignKey(to=Attractions, on_delete=models.CASCADE)

class TravelFavorite(models.Model):
    u = models.ForeignKey(to=User, on_delete=models.CASCADE)
    ct = models.ForeignKey(
        to=Create_Travel, on_delete=models.SET_DEFAULT, default=-1
    )  # 行程沒了歷史也會被刪除

class Search(models.Model):
    attractions = models.ManyToManyField(Attractions)
    IP_address = models.TextField(max_length=255, null=False, blank=False)
    keyword = ArrayField(models.TextField())
    identify = models.BooleanField(default=False)  # 0為訪客，1為會員
