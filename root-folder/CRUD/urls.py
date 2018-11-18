from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('t',views.test, name="test"),
    path('verify_user', views.verify_user, name='verify_user'),
    path('user_info', views.user_info, name='user_info'),
    path('post_comment', views.post_comment, name='post_comment')
]
