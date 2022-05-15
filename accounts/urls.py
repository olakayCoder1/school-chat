from django.urls import path
from . import views
from django.contrib.auth import views as auth_views




urlpatterns = [
    path('register/', views.register_page, name='register'),
    path('login/', views.login_page, name='login'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', views.password_reset, name='password-reset'),
    path('reset/<str:uidb64>/<str:token>/',views.password_reset_confirm, name='password_reset_confirm'),
    path('test/', views.testing)

]
