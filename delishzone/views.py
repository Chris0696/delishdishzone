from django.shortcuts import render, redirect

# from accounts.utils import userData, registrationUser


def index(request):

    return render(request, 'index.html')


def popuRegistration(request):
    return render(request, 'includes/modal_popup.html')


