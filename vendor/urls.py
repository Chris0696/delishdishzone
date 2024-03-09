from django.urls import path, include
from .import views
from accounts.views import users as AccountViews


urlpatterns = [
    path('', AccountViews.vendorDashboard, name='vendor'),
    path('profile/', views.v_profile, name='vprofile'),


]

