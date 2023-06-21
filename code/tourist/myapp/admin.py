from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(User)
class PostAdmin(admin.ModelAdmin):
    list_display=('id','name','mail')
    list_filter=('gender',)
    search_fields=('name',)
    ordering=('id',)


# @admin.register(Tag)
# class TagAdmin(admin.ModelAdmin):
#     list_display = ("name",)


# @admin.register(Comment)
# class CommentAdmin(admin.ModelAdmin):
#     list_display = ("post", "content")

# admin.site.register(User)
admin.site.register(Attractions)
admin.site.register(Crowd_Opening)
admin.site.register(Create_Travel)
admin.site.register(Attractions_Ct)
admin.site.register(History)
admin.site.register(Comment)
admin.site.register(Favorite)
admin.site.register(Search)