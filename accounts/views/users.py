from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
from django.utils.http import urlsafe_base64_decode

from ..models import User
from ..utils import detectUser, send_verification_email


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


def activate(request, uidb64, token):
    # Activate the user by setting the is_active status to True

    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulation! Your account has been activated!')
        return redirect('accounts:myAccount')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('accounts:myAccount')


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
    return render(request, 'accounts/vendordashboard.html')


def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)

            # send reset password email
            mail_subject = 'Reset your password'
            mail_template = 'accounts/emails/reset_password_email.html'
            send_verification_email(request, user, mail_subject, mail_template)

            messages.success(request, 'Password reset link has been sent to your email adress')
            return redirect('accounts:loginUser')
        else:
            messages.error(request, 'Accounts does not exist')
            return redirect('accounts:forgotPassword')

    return render(request, 'accounts/forgot_password.html')


def resetpasswordValidate(request, uidb64, token):
    # validate the user by decoding the token and user pk
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.info(request, 'Please reset your password')
        return redirect('accounts:resetPassword')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('accounts:myAccount')


def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, 'Password do not match!')
            return redirect('accounts:resetPassword')
        elif password == confirm_password and len(password) >= 8:
            pk = request.session.get('uid')
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, 'Password changed successfully!')
            return redirect('accounts:loginUser')
        else:
            messages.error(request, 'Password must be at least 8 characters long!')
            return redirect('accounts:resetPassword')
    return render(request, 'accounts/reset_password.html')








