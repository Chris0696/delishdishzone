from django.urls import path
from .views import customers, restaurants, users


app_name = 'accounts'

urlpatterns = [
    path('registerUser/', customers.registerUser, name='registerUser'),
    path('register-vendor/', restaurants.registerVendor, name='registerVendor'),

    path('login/', users.loginUser, name='loginUser'),
    path('logout/', users.logoutUser, name='logout'),

    path('myAccount/', users.myAccount, name='myAccount'),
    path('custDashboard/', users.custDashboard, name='custDashboard'),
    path('vendorDashboard/', users.vendorDashboard, name='vendorDashboard'),

]

