from django.http import HttpResponseRedirect
from django.shortcuts import render
from user.forms import SignupForm, LoginForm, ChangePasswordForm, ProfileUpdateForm
from django.contrib.auth import authenticate, login as user_login, logout as user_logout, update_session_auth_hash
from django.urls import reverse
from user.models import User, Patient


def signup(request):
    """
    Creates a new user based on given email, password and other necessary informations
    """
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            Patient.objects.create(user=user)
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
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                user_login(request, user)
                return HttpResponseRedirect(reverse("accounts:signup"))
            else:
                return HttpResponseRedirect(reverse("accounts:login"))
        else:
            return HttpResponseRedirect(reverse("accounts:login"))
    else:
        context = {
            'form': LoginForm,
        }
        return render(request, "user/login.html", context)


def logout(request):
    """
    Logout the user from the current session
    """
    user_logout(request)
    return HttpResponseRedirect(reverse("accounts:login"))


def change_password(request):
    """
    Changes the password of the user
    """
    if request.method == "POST":
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return HttpResponseRedirect(reverse("accounts:login"))
        else:
            return HttpResponseRedirect(reverse("accounts:change-password"))
    else:
        context = {
            'form': ChangePasswordForm(request.user)
        }
        return render(request, "user/change-password.html", context)


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


def profile_update(request):
    """
    Updates the profile information of user
    """
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=request.user)
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