from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.login, name="login"),
    path('user/<int:employee_id>/', views.user, name="user"),
    path('superuser/<int:employee_id>/', views.superuser, name="superuser"),
    path('handlelogin/', views.handlelogin, name= "handlelogin")
]