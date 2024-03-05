from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'accounts'

urlpatterns = [
    path('registerUser/', views.registerUser, name='registerUser'),
    path('register-restaurant/', views.registerRestaurant, name='registerRestaurant')

]

