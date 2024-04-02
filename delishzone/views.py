from django.contrib.gis.geos import GEOSGeometry
from django.db.models import Prefetch, Q
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
from django.shortcuts import render, redirect, get_object_or_404
from menu.models import Category, FoodItem
from vendor.models import Vendor



# from accounts.utils import userData, registrationUser

def get_or_set_current_location(request):
    if 'lat' in request.session:
        lat = request.session['lat']
        lng = request.session['lng']
        return lng, lat

    elif 'lat' in request.GET:
        lat = request.GET.get('lat')
        lng = request.GET.get('lng')
        request.session['lat'] = lat
        request.session['lng'] = lng
        return lng, lat
    else:
        return None


def index(request):
    if get_or_set_current_location(request) is not None:

        pnt = GEOSGeometry('POINT(%s %s)' % (get_or_set_current_location(request)))

        vendors = Vendor.objects.filter(
            user_profile__location__distance_lte=(pnt, D(km=1000))
        ).annotate(distance=Distance("user_profile__location", pnt)).order_by("distance")

        for v in vendors:
            v.kms = round(v.distance.km, 1)

    else:
        vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)[:8]

    fooditems = FoodItem.objects.filter(is_available=True)[:15]

    context = {'vendors': vendors,
               'fooditems': fooditems,
               }

    return render(request, 'index.html', context)



