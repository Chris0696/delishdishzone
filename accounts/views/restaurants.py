from django.contrib import messages, auth
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from ..forms import UserForm
from ..models import User, UserProfile

from vendor.forms import VendorForm

"""
class RegisterRestaurant(CreateView):
    model = User
    form_class = UserForm
    v_form_class = VendorForm
    template_name = 'accounts/registerUser.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'customer'
        return super().get_context_data(**kwargs)

    def form_valid(self, form, v_form):
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email,
                                        password=password)
        user.role = User.RESTAURANT
        user.save()
        user = VendorForm()
        vendor = v_form.save(commit=False)
        vendor.user = user
        user_profile = UserProfile.objects.get(user=user)
        vendor.user_profile = user_profile
        vendor.save()
        messages.success(self.request, 'Your restaurant account has been successfully registered! Please wait for the '
                                       'approuval.')
        return redirect('accounts:registerVendor')

    def v_form_valid(self, v_form):
        pass
"""


def registerVendor(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in !')
        return redirect('accounts:dashbord')
    elif request.method == 'POST':
        # store the data and create user
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)
        if form.is_valid() and v_form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name'].upper()
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
            return redirect('accounts:loginUser')
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


