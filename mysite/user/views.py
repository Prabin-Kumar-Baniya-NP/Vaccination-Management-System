from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from user.forms import SignupForm, LoginForm, ChangePasswordForm, ProfileUpdateForm
from django.contrib.auth import authenticate, login as user_login, logout as user_logout, update_session_auth_hash
from django.urls import reverse
from user.models import User
from django.contrib.auth.decorators import login_required
from user.email import send_email_verification
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from user.utils import EmailVerificationTokenGenerator


def signup(request):
    """
    Creates a new user based on given email, password and other necessary informations
    """
    if request.method == "POST":
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            send_email_verification(request, user.id)
            return HttpResponseRedirect(reverse("accounts:login"))
        else:
            return HttpResponseRedirect(reverse("accounts:signup"))
    else:
        context = {
            'form': SignupForm()
        }
        return render(request, "user/signup.html", context)


def login(request):
    """
    Login the user if the given email and password are valid
    """
    if request.method == "POST":
        form = LoginForm(request, request.POST)
        if form.is_valid():
            email = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(email=email, password=password)
            if user is not None:
                user_login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                return HttpResponseRedirect(reverse("accounts:login"))
        else:
            return HttpResponseRedirect(reverse("accounts:login"))
    else:
        context = {
            'form': LoginForm,
        }
        return render(request, "user/login.html", context)


@login_required
def logout(request):
    """
    Logout the user from the current session
    """
    user_logout(request)
    return HttpResponseRedirect(reverse("accounts:login"))


@login_required
def change_password(request):
    """
    Changes the password of the user
    """
    if request.method == "POST":
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return HttpResponseRedirect(reverse("accounts:profile-view"))
        else:
            return HttpResponseRedirect(reverse("accounts:change-password"))
    else:
        context = {
            'form': ChangePasswordForm(request.user)
        }
        return render(request, "user/change-password.html", context)


@login_required
def profile_view(request):
    """
    Displays the profile information of user
    """
    try:
        user = User.objects.get(id=request.user.id)
    except User.DoesNotExist:
        return HttpResponseRedirect(reverse("accounts:signup"))
    context = {
        'user': user
    }
    return render(request, "user/profile-view.html", context)


@login_required
def profile_update(request):
    """
    Updates the profile information of user
    """
    if request.method == "POST":
        form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("accounts:profile-view"))
        else:
            return HttpResponseRedirect(reverse("accounts:profile-update"))
    else:
        context = {
            "form": ProfileUpdateForm(instance=request.user)
        }
        return render(request, "user/profile-update.html", context)


@login_required
def email_verification_request(request):
    """
    Handles the request for email verification
    """
    if not request.user.is_email_verified:
        send_email_verification(request, request.user.id)
        return HttpResponse("Email Verification Link sent to your email address")
    else:
        return HttpResponse("Email Already Verified")


def email_verifier(request, uidb64, token):
    """
    Checks the verification link and verifies the user
    """
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and EmailVerificationTokenGenerator.check_token(user, token):
        user.is_email_verified = True
        user.save()
        return HttpResponseRedirect(reverse("accounts:profile-view"))
    else:
        return HttpResponse('Activation link is invalid!')
