from django.contrib import messages, auth
from django.shortcuts import render, redirect
from django.contrib.auth import login
from ..forms import UserForm
from ..models import User
from django.views.generic import CreateView

"""
class RegisterUser(CreateView):
    model = User
    form_class = UserForm
    template_name = 'accounts/registerUser.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'customer'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        password = form.cleaned_data['password']
        user = form.save(commit=False)
        user.set_password(password)
        user.role = User.CUSTOMER
        user.save()
        messages.success(self.request, 'User created successfully!')
        print('User is created')
        return redirect('accounts:loginUser')

"""


def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in !')
        return redirect('accounts:dashbord')
    # Create the user using the form
    elif request.method == 'POST':
        print(request.POST)
        form = UserForm(request.POST)
        if form.is_valid():
            # password = form.cleaned_data['password']
            # user = form.save(commit=False)
            # user.set_password(password)
            # user.role = User.CUSTOMER
            # user.save()

            # Create the user using create_user method

            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name'].upper()
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email,
                                            password=password)
            user.role = User.CUSTOMER
            user.save()
            messages.success(request, 'User successfully registered!')
            print('User is created')

            return redirect('accounts:loginUser')

    else:
        form = UserForm()
    context = {

        'form': form
    }
    return render(request, 'accounts/registerUser.html', context)

