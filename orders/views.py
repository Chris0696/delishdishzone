from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from marketplace.models import Cart, Tax
from marketplace.context_processors import get_cart_amounts

from .forms import OrderForm
from .models import Order, Payment, OrderedFood
import simplejson as json
from .utils import generate_order_number
from menu.models import FoodItem
from accounts.utils import send_notification
from django.contrib.auth.decorators import login_required


@login_required(login_url='accounts:loginUser')
def place_order(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created')
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('marketplace:listing')

    vendors_ids = []
    for i in cart_items:
        if i.fooditem.vendor.id not in vendors_ids:
            vendors_ids.append(i.fooditem.vendor.id)

    # {"vendor_id":{"subtotal":{"tax_type": {"tax_percentage": "tax_amount"}}}}
    get_tax = Tax.objects.filter(is_active=True)
    total_data = {}
    subtotal = 0
    k = {}
    for i in cart_items:
        fooditem = FoodItem.objects.get(pk=i.fooditem.id,
                                        vendor_id__in=vendors_ids)  # Faire afficher les produits appartenant repectivement à un fournisseur.
        v_id = fooditem.vendor.id
        print(fooditem, fooditem.vendor.restaurant_name, "Id = ", v_id)
        if v_id in k:
            subtotal = k[v_id]
            subtotal += (fooditem.price * i.quantity)
            k[v_id] = subtotal
        else:
            subtotal = (fooditem.price * i.quantity)
            k[v_id] = subtotal
        # print(k)

        # Calculate tax_data
        tax_dict = {}
        for y in get_tax:
            tax_type = y.tax_type
            tax_percentage = y.tax_percentage
            tax_amount = round((subtotal * tax_percentage) / 100, 2)
            tax_dict.update({tax_type: {str(tax_percentage): str(tax_amount)}})
        # print(tax_dict)

        # Construct Total data
        total_data.update({fooditem.vendor.id: {str(subtotal): str(tax_dict)}})
    print(total_data)

    subtotal = get_cart_amounts(request)['subtotal']
    total_tax = get_cart_amounts(request)['tax']
    grand_total = get_cart_amounts(request)['grand_total']
    tax_data = get_cart_amounts(request)['tax_dict']

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order()
            order.first_name = form.cleaned_data['first_name']
            order.last_name = form.cleaned_data['last_name']
            order.phone_number = form.cleaned_data['phone_number']
            order.email = form.cleaned_data['email']
            order.address = form.cleaned_data['address']
            order.country = form.cleaned_data['country']
            order.departement = form.cleaned_data['departement']
            order.city = form.cleaned_data['city']
            order.rue = form.cleaned_data['rue']
            order.user = request.user
            order.subtotal = subtotal
            order.total = grand_total
            order.tax_data = json.dumps(tax_data)
            order.total_data = json.dumps(total_data)
            order.total_tax = total_tax
            order.payment_method = request.POST['payment_method']
            order.save()  # order id/pk is generated
            order.order_number = generate_order_number(order.id)
            order.vendors.add(*vendors_ids)
            order.save()
            context = {
                'order': order,
                'cart_items': cart_items,
            }
            return render(request, 'orders/place_order.html', context)
        else:
            print(form.errors)
    return render(request, 'orders/place_order.html')


@login_required(login_url='accounts:loginUser')
def payments(request):
    # Check if the request is ajax or not
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
        # STORE THE PAYMENT DETAILS IN THE PAYMENT MODEL
        order_number = request.POST.get('order_number')
        transaction_id = request.POST.get('transaction_id')
        payment_method = request.POST.get('payment_method')
        status = request.POST.get('status')

        print(order_number, transaction_id, payment_method)

        order = Order.objects.get(user=request.user, order_number=order_number)
        payment = Payment(
            user=request.user,
            transaction_id=transaction_id,
            payment_method=payment_method,
            amount=order.total,
            status=status,
        )
        payment.save()

        # UPDATE THE ORDER MODEL
        order.payment = payment
        order.is_ordered = True
        order.save()

        # MOVE THE CART ITEMS TO ORDERED FOOD MODEL
        cart_items = Cart.objects.filter(user=request.user)
        for item in cart_items:
            ordered_food = OrderedFood()
            ordered_food.order = order
            ordered_food.payment = payment
            ordered_food.user = request.user
            ordered_food.fooditem = item.fooditem
            ordered_food.quantity = item.quantity
            ordered_food.price = item.fooditem.price
            ordered_food.amount = item.fooditem.price * item.quantity  # Total amount
            ordered_food.save()

        # SEND ORDER CONFIRMATION EMAIL TO THE CUSTOMER

        mail_subject = 'Thank you for ordering with us'
        mail_template = 'orders/order_confirmation_email.html'
        context = {
            'user': request.user,
            'order': order,
            'to_email': order.email,
        }
        send_notification(mail_subject, mail_template, context)

        # SEND ORDER RECEIVED EMAIL TO THE VENDOR
        mail_subject = 'You have receved a new order,'
        mail_template = 'orders/new_order_received_email.html'
        to_emails = []
        for i in cart_items:
            if i.fooditem.vendor.user.email not in to_emails:
                to_emails.append(i.fooditem.vendor.user.email)
        print("to_emails === > ", to_emails)

        context = {
            'order': order,
            'to_email': to_emails,
        }
        send_notification(mail_subject, mail_template, context)

        # CLEAR THE CART IF THE PAYMENT IS SUCCESS

        cart_items.delete()

        # RETURN BACK TO AJAX WITH THE STATUS SUCCESS OR FAILURE
        response = {
            'order_number': order_number,
            'transaction_id': transaction_id
        }

        return JsonResponse(response)

    return HttpResponse('Payments Status')


def order_completed(request):
    order_number = request.GET.get('order_no')
    transaction_id = request.GET.get('trans_id')

    try:
        order = Order.objects.get(order_number=order_number, payment__transaction_id=transaction_id, is_ordered=True)
        ordered_food = OrderedFood.objects.filter(order=order)

        subtotal = 0
        for item in ordered_food:
            subtotal += (item.quantity * item.price)

        tax_data = json.loads(order.tax_data)
        print(tax_data)
        context = {
            'order': order,
            'ordered_food': ordered_food,
            'subtotal': subtotal,
            'tax_data': tax_data,
        }
        return render(request, 'orders/order_completed.html', context)

    except:
        return redirect('index')
