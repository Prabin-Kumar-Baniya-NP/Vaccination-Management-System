import logging
from django.http import (
    HttpResponseRedirect,
    HttpResponse,
    HttpResponseForbidden,
    HttpResponseBadRequest,
)
from django.shortcuts import render
from user.forms import (
    SignupForm,
    LoginForm,
    ChangePasswordForm,
    ProfileUpdateForm,
    PasswordResetForm,
    SetPasswordForm,
)
from django.contrib.auth import (
    authenticate,
    login as user_login,
    logout as user_logout,
    update_session_auth_hash,
)
from django.urls import reverse, reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from user.email import send_email_verification
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from user.utils import EmailVerificationTokenGenerator
from django.contrib import messages
from django.contrib.auth import views as DefaultAuthViews


User = get_user_model()

logger = logging.getLogger("django")


def signup(request):
    """
    Creates a new user based on given email, password and other necessary informations
    """
    if request.method == "POST":
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            send_email_verification(request, user.id)
            logger.info("New user Created")
            messages.success(
                request,
                "Account Created Successfully ! Please enter the email and password to login",
            )
            return HttpResponseRedirect(reverse("accounts:login"))
        else:
            logger.error("Invalid Signup Data")
            messages.error(request, "Please Enter Valid Data")
            return render(request, "user/signup.html", {"form": form})
    else:
        context = {"form": SignupForm()}
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
                logger.info("User Logged in")
                messages.success(request, "Logged in Successfully")
                return HttpResponseRedirect(reverse("index"))
            else:
                logger.error("User is None")
                messages.error(request, "Invalid Login! Please enter correct data")
                return HttpResponseRedirect(reverse("accounts:login"))
        else:
            logger.error("Invalid Username and Passsword")
            messages.error(request, "Please Enter Correct Username and Password")
            return render(request, "user/login.html", {"form": form})
    else:
        context = {
            "form": LoginForm,
        }
        a = 1/0
        return render(request, "user/login.html", context)


def logout(request):
    """
    Logout the user from the current session
    """
    user_logout(request)
    logger.info("Logged out successfully")
    messages.info(request, "Logged out successfully")
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
            logger.info("Password Changed")
            messages.success(request, "Password Changed Successfully")
            return HttpResponseRedirect(reverse("accounts:profile-view"))
        else:
            logger.error("Invalid Data")
            messages.error(
                request, "Unable to change password! Please enter valid data"
            )
            return render(request, "user/change-password.html", {"form": form})
    else:
        context = {"form": ChangePasswordForm(request.user)}
        return render(request, "user/change-password.html", context)


@login_required
def profile_view(request):
    """
    Displays the profile information of user
    """
    context = {"user": request.user}
    return render(request, "user/profile-view.html", context)


@login_required
def profile_update(request):
    """
    Updates the profile information of user
    """
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            logger.info("Profile Information Updated")
            messages.success(request, "Profile Information Updated Successfully")
            return HttpResponseRedirect(reverse("accounts:profile-view"))
        else:
            logger.error("Invalid Data")
            messages.error(request, "Invalid Data! Please enter correct data")
            return render(request, "user/profile-update.html", {"form": form})
    else:
        context = {"form": ProfileUpdateForm(instance=request.user)}
        return render(request, "user/profile-update.html", context)


@login_required
def email_verification_request(request):
    """
    Handles the request for email verification
    """
    if not request.user.is_email_verified:
        send_email_verification(request, request.user.id)
        logger.info("Email Verification Link Sent")
        return HttpResponse("Email Verification Link sent to your email address")
    else:
        logger.warning("Email Already Verified")
        return HttpResponseForbidden("Email Already Verified")


def email_verifier(request, uidb64, token):
    """
    Checks the verification link and verifies the user
    """
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user == request.user:
        if EmailVerificationTokenGenerator.check_token(user, token):
            user.is_email_verified = True
            user.save()
            logger.info("Account Verified")
            messages.success(request, "Email Address Verified Successfully")
            return HttpResponseRedirect(reverse("accounts:profile-view"))
        else:
            logger.warning("Activation Link is invalid")
            return HttpResponseBadRequest("Activation link is invalid!")
    else:
        return HttpResponseForbidden(
            content="You don't have permission to use this link"
        )


class PasswordResetView(DefaultAuthViews.PasswordResetView):
    """
    Sends Password Reset Email
    """

    email_template_name = "user/password-reset-email.html"
    form_class = PasswordResetForm
    success_url = reverse_lazy("accounts:password-reset-done")
    template_name = "user/password-reset.html"


class PasswordResetDoneView(DefaultAuthViews.PasswordResetDoneView):
    """
    Handles the message for Password Email Send Request
    """

    template_name = "user/password-reset-done.html"


class PasswordResetConfirmView(DefaultAuthViews.PasswordResetConfirmView):
    """
    Checks the given token and asks for new password
    """

    form_class = SetPasswordForm
    template_name = "user/password-reset-confirm.html"
    success_url = reverse_lazy("accounts:password-reset-complete")


class PasswordResetCompleteView(DefaultAuthViews.PasswordResetCompleteView):
    """
    Shows a message for password reset status
    """

    template_name = "user/password-reset-complete.html"
