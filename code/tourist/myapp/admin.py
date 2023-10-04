from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as _UserAdmin
# Register your models here.



# 使用者---------------------------------------
class UserAdmin(_UserAdmin):
    #顯示哪些欄位
    list_display = ['email','username','gender', 'birthday', 'date_joined', 'is_superuser', 'is_staff',
                    'is_active']
    #可篩選的欄位
    list_filter= ('gender','date_joined', 'is_superuser', 'is_active')

    #可搜尋的欄位
    search_fields = ['email', 'username', 'date_joined','gender']

    # 新增、詳細畫面
    fieldsets = (
        ('基本資料', {'fields': ('email', 'username', 'password','gender','birthday')}),
        ('權限管理', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')}),
        ('登入狀態', {'fields': ('date_joined', 'last_login')}),
    )
    # add_fieldsets = (
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': ('email', 'username', 'unit', 'contact', 'password1', 'password2'),
    #     }),
    # )
admin.site.register(User,UserAdmin)
admin.site.site_header = 'TripFunChill_Manage'
admin.site.index_title = 'manage'

# 景點資料---------------------------------------
class AttractionsAdmin(admin.ModelAdmin):
    list_display=('id','a_name','address','phone','rating','stay_time')
    ordering=('id',)
admin.site.register(Attractions,AttractionsAdmin)

# 景點營業時間與人潮資訊 ---------------------------------------
class Crowd_OpeningAdmin(admin.ModelAdmin):
    list_display=('id','week','crowd','opening','a_id')
    ordering=('id',)
admin.site.register(Crowd_Opening,Crowd_OpeningAdmin)

# 建立行程首頁資訊----------------------------------------------
class Create_TravelAdmin(admin.ModelAdmin):
    list_display=('id','ct_name','start_day','travel_day','u_id')
    ordering=('id',)
admin.site.register(Create_Travel,Create_TravelAdmin)

# 建立行程儲存天數資訊------------------------------------------
class ChoiceDay_CtAdmin(admin.ModelAdmin):
    list_display=('id','ct_id','day','start_location_x','start_location_y','start_time')
    ordering=('id',)
admin.site.register(ChoiceDay_Ct,ChoiceDay_CtAdmin)

# 建立行程儲存景點資訊------------------------------------------
class Attractions_CtAdmin(admin.ModelAdmin):
    list_display=('id','a_start_time','stay_time','order','a_id','choice_ct_id')
    ordering=('id',)
admin.site.register(Attractions_Ct,Attractions_CtAdmin)

# 我的行程------------------------------------------------------
class HistoryAdmin(admin.ModelAdmin):
    list_display=('id','status','like','ct_id')
    ordering=('id',)
admin.site.register(History,HistoryAdmin)

# 評論----------------------------------------------------------
class CommentAdmin(admin.ModelAdmin):
    list_display=('id','u_id','a_id','h_id','score','comment_type')
admin.site.register(Comment,CommentAdmin)

# 我的最愛-------------------------------------------------------
class FavoriteAdmin(admin.ModelAdmin):
    list_display=('id','a_id','u_id')
    ordering=('id',)
admin.site.register(Favorite,FavoriteAdmin)

# 搜尋紀錄-------------------------------------------------------
class SearchAdmin(admin.ModelAdmin):
    list_display=('id','IP_address','keyword','identify')
admin.site.register(Search,SearchAdmin)

