from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from user.models import User

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["email", "first_name", "middle_name", "last_name", "date_of_birth", "gender"]
        labels = {
            "email": "Email Address"
        }

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = "__all__"

class ChangePasswordForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = "__all__"