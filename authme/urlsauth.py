from django.contrib import admin
from django.urls import include, path
from . import views


app_name = 'authme'
urlpatterns = [
    path('',views.register, name ='register'),
    path('login/', views.login_page, name ='login'),
    path('logout/', views.logout_page, name ='logout')
]
