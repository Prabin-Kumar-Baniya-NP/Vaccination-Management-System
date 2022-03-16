from django.http import HttpResponseRedirect
from django.shortcuts import render
from user.forms import SignupForm, LoginForm, ChangePasswordForm
from django.contrib.auth import authenticate, login as user_login, logout as user_logout, update_session_auth_hash
from django.urls import reverse


def signup(request):
    """
    Creates a new user based on given email, password and other necessary informations
    """
    if request.method == "POST":
        new_user = SignupForm(request.POST)
        if new_user.is_valid():
            new_user.save()
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
            user = authenticate(username=email, password=password)
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
            return HttpResponseRedirect(reverse("accounts:change_password"))
    else:
        context = {
            'form': ChangePasswordForm(request.user)
        }
        return render(request, "user/change_password.html", context)
