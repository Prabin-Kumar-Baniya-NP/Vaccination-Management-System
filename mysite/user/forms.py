from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from user.models import User, Agent
from django.forms import ModelForm


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "middle_name",
                  "last_name", "date_of_birth", "gender"]


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = "__all__"


class ChangePasswordForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = "__all__"


class ProfileUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "middle_name", "last_name", "gender",
                  "date_of_birth", "identity_document_type", "identity_document_number"]


class AgentCreateForm(ModelForm):
    class Meta:
        model = Agent
        fields = "__all__"

class AgentUpdateForm(ModelForm):
    class Meta:
        model = Agent
        fields = "__all__"
