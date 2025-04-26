from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.login, name="login"),
    path('user/', views.user, name="user"),
    path('superuser/', views.superuser, name="superuser")
]