import uuid

from django.db import models

from vendor.models import Vendor


class Category(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=180, unique=True)
    image = models.ImageField(upload_to="foodimages/food_categories", default="foodimages/food_categories/default.jpg",
                              blank=True, null=True)
    description = models.TextField(max_length=250, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def clean(self):
        self.category_name = self.category_name.capitalize()

    def __str__(self):
        return f"{self.category_name}"


class FoodItem(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="fooditems")
    food_title = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=180, unique=True)
    description = models.TextField(max_length=250, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='foodimages', default="foodimages/default.jpg")
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.food_title
