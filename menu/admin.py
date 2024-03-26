from django.contrib import admin

from .models import Category, FoodItem


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'vendor', 'created_at', 'updated_at')
    search_fields = ('category_name', 'vendor__restaurant_name')
    prepopulated_fields = {'slug': ('category_name',)}


class FoodItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('food_title',)}
    list_display = ('food_title', 'category', 'vendor', 'price', 'is_available', 'updated_at')
    search_fields = ('food_title', 'category__name', 'vendor__restaurant_name', 'price')
    list_filter = ('is_available',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(FoodItem, FoodItemAdmin)
