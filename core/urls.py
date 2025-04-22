from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('',views.index, name='index'),
    path('convert/', views.convert, name='convert'),
    path('convert/response/', views.response, name='response'),
]
