from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin


class CustomerUserAdmin(UserAdmin):
    list_display = ('first_name', 'last_name', 'username', 'email', 'role', 'phone_number', 'is_active')
    ordering = ('date_joined',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'country', 'city', 'state', 'address', 'pin_code')


admin.site.register(User, CustomerUserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
