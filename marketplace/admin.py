from django.contrib import admin

from marketplace.models import Cart, Tax, Delivery


class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'fooditem', 'quantity', 'created', 'updated')


class TaxAdmin(admin.ModelAdmin):
    list_display = ('tax_type', 'tax_percentage', 'is_active')


class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('delivery_type', 'delivery_value', 'is_active')


admin.site.register(Cart, CartAdmin)

admin.site.register(Tax, TaxAdmin)

admin.site.register(Delivery, DeliveryAdmin)
