from django.urls import path
from . import views



urlpatterns = [
    path('', views.index, name='index'),
    # path('account/register/', views.register_page, name='register'),
    # path('account/login/', views.login_page, name='login'),
    path('chat/group/<str:room_name>/', views.group_chat , name='group_chat'),
    path('chat/group/create/<str:room_name>/', views.group_chat , name='create_group_chat'),
    path('chat/group/about/<str:room_name>/', views.group_about, name='about_group_chat'),
    path('chat/<str:username>/', views.direct_chat, name='direct_chat')

] 