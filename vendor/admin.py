from django.contrib import admin
from .models import Vendor


class VendorAdmin(admin.ModelAdmin):
    list_display = ('user', 'restaurant_name', 'restaurant_address', 'restaurant_phone', 'restaurant_license', 'is_approved', 'created_at')


admin.site.register(Vendor, VendorAdmin)
