from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
from django.db.models import Prefetch, Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from vendor.models import Vendor

from menu.models import Category, FoodItem

from .context_processors import get_cart_counter, get_cart_amounts
from .models import Cart
from accounts.views.users import check_role_customer


def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)[:8]

    vendor_count = vendors.count()

    context = {
        'vendors': vendors,
        'vendor_count': vendor_count
    }
    return render(request, 'marketplace/listing.html', context)


def marketplace_detail(request, slug):
    vendor = get_object_or_404(Vendor, slug=slug)

    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'fooditems',
            queryset=FoodItem.objects.filter(is_available=True)
        )
    )

    if request.user.is_authenticated:
        cartitems = Cart.objects.filter(user=request.user)
    else:
        cartitems = None

    context = {
        'vendor': vendor,
        'categories': categories,
        'cartitems': cartitems,
    }
    return render(request, 'marketplace/restaurant_detail.html', context)


def add_to_cart(request, food_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Check if the food item exists.
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                # Check if user has already added that food to the cart
                try:
                    checkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    # Increase the cart quantity
                    checkCart.quantity += 1
                    checkCart.save()
                    return JsonResponse({'status': 'Success', 'message': 'Increased the cart quantity !',
                                         'cart_counter': get_cart_counter(request), 'qty': checkCart.quantity,
                                         'cart_amount': get_cart_amounts(request)})
                except:
                    checkCart = Cart.objects.create(user=request.user, fooditem=fooditem, quantity=1)
                    return JsonResponse({'status': 'Success', 'message': 'Added the food to the cart !',
                                         'cart_counter': get_cart_counter(request), 'qty': checkCart.quantity,
                                         'cart_amount': get_cart_amounts(request)})
            except:
                return JsonResponse({'status': 'failed', 'message': 'This food does not exist !'})
        else:
            JsonResponse({'status': 'failed', 'message': 'Invalid request !'})
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})


@user_passes_test(check_role_customer)
def decrease_cart(request, food_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Check if the food item exists.
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                # Check if user has already added that food to the cart
                try:
                    checkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    if checkCart.quantity > 1:
                        # decrease the cart quantity
                        checkCart.quantity -= 1
                        checkCart.save()
                    else:
                        checkCart.delete()
                        checkCart.quantity = 0
                    return JsonResponse(
                        {'status': 'Success', 'cart_counter': get_cart_counter(request), 'qty': checkCart.quantity,
                         'cart_amount': get_cart_amounts(request)})
                except:
                    return JsonResponse({'status': 'Failed', 'message': "You don't have this item in your cart !"})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'This food does not exist !'})
        else:
            JsonResponse({'status': 'Failed', 'message': 'Invalid request !'})
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})


@login_required(login_url='accounts:loginUser')
@user_passes_test(check_role_customer)
def cart(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created')

    context = {'cart_items': cart_items}
    return render(request, 'marketplace/cart.html', context)


def delete_cart(request, cart_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                # Check if the cart items exist
                cart_item = Cart.objects.get(user=request.user, id=cart_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse(
                        {'status': 'Success', 'message': 'Cart item has been deleted.',
                         'cart_counter': get_cart_counter(request), 'cart_amount': get_cart_amounts(request)})
            except:
                return JsonResponse({'status': 'Failed', 'message': "Cart Item does'nt exist !"})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalide requets !'})


def search(request):
    if not 'adress' in request.GET:
        return redirect('marketplace:listing')
    else:
        address = request.GET['address']
        longitude = request.GET['lng']
        latitude = request.GET['lat']
        radius = request.GET['radius']
        keyword = request.GET['keyword']

    #  get vendor ids that food item the user is looking for
    fetch_vendors_by_fooditems = FoodItem.objects.filter(food_title__icontains=keyword, is_available=True).values_list(
        'vendor', flat=True)

    vendors = Vendor.objects.filter(
        Q(id__in=fetch_vendors_by_fooditems) | Q(restaurant_name__icontains=keyword, is_approved=True,
                                                 user__is_active=True))

    if longitude and latitude and radius:
        pnt = GEOSGeometry('POINT(%s %s)' % (longitude, latitude))

        vendors = Vendor.objects.filter(
            Q(id__in=fetch_vendors_by_fooditems) | Q(restaurant_name__icontains=keyword, is_approved=True,
                                                     user__is_active=True),
            user_profile__location__distance_lte=(pnt, D(km=radius))
        ).annotate(distance=Distance("user_profile__location", pnt)).order_by("distance")

        for v in vendors:
            v.kms = round(v.distance.km, 1)

    vendor_count = vendors.count()

    context = {
        'vendors': vendors,
        'vendor_count': vendor_count,
        'source_location': address,
    }
    return render(request, 'marketplace/listing.html', context)
