from django.urls import path
from accounts.views import users as AccountViews
from . import views

urlpatterns = [
    path('', AccountViews.custDashboard, name='customer'),
    path('profile/', views.cprofile, name='cprofile'),
    path('my_orders/', views.my_orders, name='customer_orders'),
    path('orders_details/<int:order_number>/', views.orders_details, name='orders_details'),
]






