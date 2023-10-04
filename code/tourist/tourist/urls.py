"""tourist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import old_views as old_views
from myapp.views import (
    index,
    login,
    forget_pwd,
    register,
    create_index,
    create,
    history,
    favorite,
    attraction_details,
)


# from myapp.views import sayhello,get_all_taiwan,opentime #新增

urlpatterns = [
    path("admin/", admin.site.urls),
    # path('sayhello/',views.sayhello),#測試
    # path('test/',views.get_all_taiwan),#測試
    # path('opentime/',views.opentime), #測試
    # path('admin_index/',views.admin_index),
    # path('admin_login/',views.admin_login),
    # path('admin_manageuser/',views.admin_manageuser),
    # path('admin_comment/',views.admin_comment),
    path("", index.index),
    path("login/", login.login),
    path("logout/", login.logout),
    path("forget_passwd/", forget_pwd.forget_passwd, name="forget_passwd"),
    path("reset_passwd/", forget_pwd.reset_passwd, name="reset_passwd"),
    path("register/", register.register),
    path("register_verification/<str:token>/", register.register_verification),
    path("search/", old_views.search),
    path("createindex/", create_index.create_index),
    # path('create/<int:ct_id>/<int:choiceday>',views.create),
    path("create/<int:ct_id>", create.create),
    path("history/", history.history),
    path("favorite/", favorite.favorite),
    path("share/", old_views.share),
    path("attraction_details/", attraction_details.attraction_details, name="search_results"),
    path("attraction_details/<int:aid>", attraction_details.attraction_details),
    path(
        "serach_results_att_type",
        attraction_details.attraction_details_att_type,
        name="serach_results_att_type",
    ),
    # path('test/',views.test_input),
    path("useredit/", old_views.user_edit),
    path("add_favorite/", favorite.add_favorite),  # 沒有頁面
    path("del_favorite/<int:a_id>", favorite.del_favorite),  # 沒有頁面
    # path('attraction_details/<int:a_id>',views.attraction_details),
    # path('sayhello/<str:username>',sayhello), #新增
]
