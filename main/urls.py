from django.contrib import admin
from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required
urlpatterns = [
    path('register/',register,name="register"),
    path('',scrape_home,name='home')
]