from .models import Cart, Tax, Delivery
from menu.models import FoodItem


def get_cart_counter(request):
    cart_count = 0
    if request.user.is_authenticated:
        try:
            cart_items = Cart.objects.filter(user=request.user)
            if cart_items:
                for cart_item in cart_items:
                    cart_count += cart_item.quantity
            else:
                cart_count = 0
        except:
            cart_count = 0
    return dict(cart_count=cart_count)


def get_cart_amounts(request):
    subtotal = 0
    tax = 0
    delivery = 0
    grand_total = 0
    g_total = 0
    delivery_dict = {}
    tax_dict = {}

    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        for item in cart_items:
            fooditem = FoodItem.objects.get(pk=item.fooditem.id)
            subtotal += fooditem.price * item.quantity

        get_delivery = Delivery.objects.filter(is_active=True)
        for i in get_delivery:
            delivery_type = i.delivery_type
            delivery_value = i.delivery_value
            delivery_price = delivery_value

            delivery_dict.update({delivery_type: {str(delivery_value): delivery_price}})

        get_tax = Tax.objects.filter(is_active=True)
        for i in get_tax:
            tax_type = i.tax_type
            tax_percentage = i.tax_percentage
            tax_amount = round((subtotal * tax_percentage) / 100, 2)

            tax_dict.update({tax_type: {str(tax_percentage): tax_amount}})

        tax = sum(x for key in tax_dict.values() for x in key.values())

        delivery = sum(x for key in delivery_dict.values() for x in key.values())

        grand_total += subtotal + tax + delivery
        g_total = round(grand_total)
    print(tax_dict)
    print(subtotal)
    print(grand_total)
    print(g_total)

    return dict(subtotal=subtotal, tax=tax, delivery=delivery, grand_total=grand_total, delivery_dict=delivery_dict,
                tax_dict=tax_dict, g_total=g_total)
