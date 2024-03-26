from django.shortcuts import render, redirect

from vendor.models import Vendor


# from accounts.utils import userData, registrationUser


def index(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)[:8]
    context = {'vendors': vendors}
    return render(request, 'index.html', context)


def popuRegistration(request):
    return render(request, 'includes/modal_popup.html')


