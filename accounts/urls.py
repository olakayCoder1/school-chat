from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout



urlpatterns = [
    path('register/', views.register_page, name='register'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_views , name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', views.password_reset_retrieve, name='password-reset'),
    path('reset/<str:uidb64>/<str:token>/',views.password_reset_confirm_retrieve, name='password_reset_confirm'),
    path('profile/', views.account_profile, name='settings'),
    path('profile/settings/', views.account_profile_settings, name='settings'),



    path('test/', views.testing)

]
