from django.urls import path, include
from . import views
from accounts.views import users as AccountViews

urlpatterns = [
    path('', AccountViews.vendorDashboard, name='vendor'),
    path('profile/', views.v_profile, name='vprofile'),
    path('menu-builder/', views.menuBuilder, name='menu_builder'),

    # Category CRUD
    path('menu-builder/category/<int:pk>/', views.foodItems_by_category, name='fooditems_by_category'),
    path('menu-builder/category/add/', views.add_category, name='add_category'),
    path('menu-builder/category/edit/<int:pk>/', views.edit_category, name='edit_category'),
    path('menu-builder/category/delete/<int:pk>/', views.delete_category, name='delete_category'),

    # FoodItem
    path('menu-builder/food/add/', views.add_food, name='add_food'),
    path('menu-builder/food/edit/<int:pk>/', views.edit_food, name='edit_food'),
    path('menu-builder/food/delete/<int:pk>/', views.delete_food, name='delete_food'),

    # Opening Hour CRUD
    path('opening-hours/', views.opening_hours, name='opening_hours'),
    path('opening-hours/add/', views.add_opening_hours, name='add_opening_hours'),
    path('opening-hours/remove/<int:pk>/', views.remove_opening_hours, name='remove_opening_hours'),

    # Order Details
    path('orders_details/<int:order_number>/', views.orders_details, name='vendor_orders_details'),
    path('my_orders/', views.my_orders, name='vendor_my_orders'),

]
