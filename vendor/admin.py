from django.contrib import admin
from .models import Vendor, OpeningHour


class VendorAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'restaurant_name', 'restaurant_address', 'restaurant_phone', 'restaurant_license', 'is_approved',
        'created_at')
    list_filter = ('is_approved',)
    list_editable = ('is_approved',)
    prepopulated_fields = {'slug': ('restaurant_name',)}


class OpeningHourAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'day', 'from_hour', 'to_hour')


admin.site.register(Vendor, VendorAdmin)

admin.site.register(OpeningHour, OpeningHourAdmin)
