from django.db import models
from accounts.models import User
from menu.models import FoodItem
from vendor.models import Vendor
import json
request_object = ''


class Payment(models.Model):
    PAYMENT_METHOD = (
        ('Paypal', 'PayPal'),
        ('RazorPay', 'RazorPay'),  # Only for India Students.
        ('MomoPay', 'MomoPay'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100)
    payment_method = models.CharField(choices=PAYMENT_METHOD, max_length=100)
    amount = models.CharField(max_length=10)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.transaction_id


class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    vendors = models.ManyToManyField(Vendor, blank=True)
    order_number = models.CharField(max_length=25)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15, blank=True)
    email = models.EmailField(max_length=50)
    address = models.CharField(max_length=200)
    country = models.CharField(max_length=15, blank=True)
    rue = models.CharField(max_length=50, blank=True, null=True)
    departement = models.CharField(max_length=35, blank=True, null=True)
    state = models.CharField(max_length=25, blank=True)
    city = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)
    total = models.FloatField()
    tax_data = models.JSONField(blank=True, help_text="Data format: {'tax_type':{'tax_percentage':'tax_amount'}}",
                                null=True)
    total_data = models.JSONField(blank=True, null=True)
    total_tax = models.FloatField()
    payment_method = models.CharField(max_length=30)
    status = models.CharField(max_length=20, choices=STATUS, default='New')
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Concatenate first name and last name

    @property
    def name(self):
        return f'{self.first_name} {self.last_name}'

    def order_placed_to(self):
        return ", ".join([str(i) for i in self.vendors.all()])

    def get_total_by_vendor(self):
        vendor = Vendor.objects.get(user=request_object.user)
        subtotal = 0
        tax = 0
        tax_dict = {}

        if self.total_data:
            total_data = json.loads(self.total_data)
            # print(total_data)
            data = total_data.get(str(vendor.id))

            for key, val in data.items():
                # print('inform : ',  key, val)
                subtotal += float(key)
                # print("val = ", val)
                val = val.replace("'", '"')
                val = json.loads(val)
                tax_dict.update(val)
                # print('subtotal = ', subtotal)
                # print('tax_dict = ', tax_dict)

                # Calculate tax
                # {'Livraison en local': {'8.00': '79.92'}, 'Livraison en ville': {'20.00': '199.80'}}
                for x in val:
                    for w in val[x]:
                        # print(val[x][w])
                        tax += float(val[x][w])
                        # print('tax =', tax)
        grand_total = float(subtotal) + float(tax)
        # print("subtotal === ", subtotal)
        # print("tax_dict === ", tax_dict)
        # print("tax === ", tax)
        # print("grand_total === ", grand_total)

        context = {
            'subtotal': subtotal,
            'tax_dict': tax_dict,
            'grand_total': grand_total,
        }

        return context

    def __str__(self):
        return self.order_number


class OrderedFood(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fooditem = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.fooditem.food_title
