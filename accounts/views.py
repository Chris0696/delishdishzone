from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import UserForm
from .models import User, UserProfile
from .utils import registrationUser
from vendor.forms import VendorForm


# from .utils import registrationUser


def registerUser(request):
    # Create the user using the form
    if request.method == 'POST':
        print(request.POST)
        form = UserForm(request.POST)
        if form.is_valid():
            """
            password = form.cleaned_data['password']
            user = form.save(commit=False)
            user.set_password(password)
            user.role = User.CUSTOMER
            user.save()

            """
            # Create the user using create_user method

            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email,
                                            password=password)
            user.role = User.CUSTOMER
            user.save()
            messages.success(request, 'User successfully registered!')
            print('User is created')

            return redirect('accounts:registerUser')

    else:
        userdata = registrationUser(request)
        form = userdata['form']
    context = {
        'form': form
    }
    return render(request, 'accounts/registerUser.html', context)


def registerVendor(request):
    if request.method == 'POST':
        # store the data and create user
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)
        if form.is_valid() and v_form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email,
                                            password=password)
            user.role = User.RESTAURANT
            user.save()
            vendor = v_form.save(commit=False)
            vendor.user = user
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()
            messages.success(request, 'Your restaurant account has been successfully registered! Please wait for the '
                                      'approuval.')
            return redirect('accounts:registerVendor')
        else:
            print('invalid form')
            print(form.errors)
    else:
        form = UserForm()
        v_form = VendorForm()

    context = {
        'form': form,
        'v_form': v_form,
    }

    return render(request, 'accounts/registerVendor.html', context)


"""
def registerRestaurant(request):
    # Create the user using the form
    if request.method == 'POST':
        print(request.POST)
        usertype = userData(request)
        return usertype
    else:
        userdata = registrationUser(request)
        form = userdata['form']
    context = {
        'form': form
    }
    return render(request, 'accounts/register-restaurant.html', context)
"""
