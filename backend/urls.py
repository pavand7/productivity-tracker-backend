"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include, re_path
from .router import router
from userapi.views import addComment, createTables, deleteComment, getLastWeekProductivity ,likeComment, likePost, unLikeComment, unLikePost

urlpatterns = [
    path('admin/', admin.site.urls),
    # re_path('api/likePost/$', likePost, name = 'like_post'),
    re_path(r'api/likePost/(?P<postID>\d+)/(?P<userID>\d+)/', likePost, name = 'like_post'),
    re_path(r'api/unLikePost/(?P<postID>\d+)/(?P<userID>\d+)/', unLikePost, name = 'unLike_post'),
    re_path(r'api/likeComment/(?P<commentID>\d+)/(?P<userID>\d+)/', likeComment, name = 'like_comment'),
    re_path(r'api/unLikeComment/(?P<commentID>\d+)/(?P<userID>\d+)/', unLikeComment, name = 'unLike_comment'),
    re_path(r'api/addComment/', addComment, name = 'add_comment'),
    re_path(r'api/deleteComment/', deleteComment, name = 'delete_comment'),
    re_path(r'api/lastWeekProductivity/(?P<userID>\d+)/', getLastWeekProductivity, name = 'last_week_productivity'),
    path('createTables/', createTables, name = 'create_tables'),
    path('api/', include(router.urls))
]