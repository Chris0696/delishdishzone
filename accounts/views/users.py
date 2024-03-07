from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
from ..utils import detectUser


# Restrict the vendor from accessing the customer page


def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied


# Restrict the customer from accessing the vendor page


def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied


def loginUser(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in !')
        return redirect('accounts:myAccount')
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(username=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, "You're now logged in")
            return redirect('accounts:myAccount')
        else:
            messages.error(request, "Invalid login credentials")
            return redirect('accounts:loginUser')

    return render(request, 'accounts/login.html')


def logoutUser(request):
    auth.logout(request)
    messages.info(request, "You're logged out")
    return redirect('accounts:loginUser')


@login_required(login_url='accounts:loginUser')
def myAccount(request):
    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)


@login_required(login_url='accounts:loginUser')
@user_passes_test(check_role_customer)
def custDashboard(request):
    return render(request, 'accounts/custdashboard.html')


@login_required(login_url='accounts:loginUser')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    return render(request, 'accounts/vendordashbord.html')
