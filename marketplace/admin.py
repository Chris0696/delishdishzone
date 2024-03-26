from django.contrib import admin

from marketplace.models import Cart


class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'fooditem', 'quantity', 'created', 'updated')


admin.site.register(Cart, CartAdmin)
