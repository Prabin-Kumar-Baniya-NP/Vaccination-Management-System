from django.urls import path
from user import views

app_name = "user"

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("change-password/", views.change_password, name="change-password"),
    path("profile-view/", views.profile_view, name="profile-view"),
    path("profile-update/", views.profile_update, name="profile-update"),
    path("verify-email/", views.email_verification_request, name="verify-email"),
    path('email/activate/<uidb64>/<token>/',
         views.email_verifier, name='email-activate'),
    path("password-reset/", views.PasswordResetView.as_view(), name="password-reset"),
    path("password-reset-done/", views.PasswordResetDoneView.as_view(), name="password-reset-done"),
    path("password-reset-confirm/<uidb64>/<token>/", views.PasswordResetConfirmView.as_view(), name="password-reset-confirm"),
    path("password-reset-complete/", views.PasswordResetCompleteView.as_view(), name="password-reset-complete"),
]
