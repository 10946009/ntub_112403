from django.contrib import admin
from .models import *

from django.contrib.auth.admin import UserAdmin as _UserAdmin
# Register your models here.

from django.contrib.auth.forms import UserCreationForm
from django.forms import forms


class UserAdmin(_UserAdmin):
    #顯示哪些欄位
    list_display = ['email', 'password','username','gender','birthday', 'date_joined', 'is_superuser', 'is_staff',
                    'is_active']
    #可篩選的欄位
    list_filter= ('gender','birthday','date_joined')

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

# @admin.register(User)
# class PostAdmin(admin.ModelAdmin):
#     list_display=('id','name','mail')
#     list_filter=('gender',)
#     search_fields=('name',)
#     ordering=('id',)


# @admin.register(Tag)
# class TagAdmin(admin.ModelAdmin):
#     list_display = ("name",)


# @admin.register(Comment)
# class CommentAdmin(admin.ModelAdmin):
#     list_display = ("post", "content")

# admin.site.register(User)

class AttractionsAdmin(admin.ModelAdmin):
    list_display=('id','a_name','address','phone','rating')
    ordering=('id',)
admin.site.register(Attractions,AttractionsAdmin)


admin.site.register(Crowd_Opening)
admin.site.register(Create_Travel)
admin.site.register(Attractions_Ct)
admin.site.register(History)
admin.site.register(Comment)
admin.site.register(Favorite)
admin.site.register(Search)