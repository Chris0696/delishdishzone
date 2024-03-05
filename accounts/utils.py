from django.shortcuts import redirect
from .forms import UserForm
from .models import User


def registrationUser(request):
    form = UserForm()
    return {'form': form}

"""

def userData(request):
    form = UserForm(request.POST)
    if form.is_valid():
        
        password = form.cleaned_data['password']
        user = form.save(commit=False)
        user.set_password(password)
        user.role = User.CUSTOMER
        user.save()

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
        print('User is created')

        return redirect('registerUser')

    return {'form': form}
"""
