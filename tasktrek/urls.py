from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.login, name="login"),
    path('signup/',views.signup_view, name='singup'),
    path('user/<int:employee_id>/', views.user, name="user"),
    path('superuser/<int:employee_id>/', views.superuser, name="superuser"),
    path('handlelogin/', views.handlelogin, name= "handlelogin"),
    path('handledelete/admin/<int:admin_id>/employee/<int:employee_id>/task/<int:task_id>/', views.handledelete, name="handledelete"),
    path('handlecreate/admin/<int:admin_id>', views.handlecreate, name="handlecreate"),
    path('handleedit/', views.handleedit, name="handleedit"),
    path('handlecomplete/', views.handlecomplete, name="handlecomplete"),
    path('handlesignup/', views.handlesignup, name="handlesignup"),
]