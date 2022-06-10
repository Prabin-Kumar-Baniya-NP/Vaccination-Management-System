from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from user.models import User
from django.forms import ModelForm
from django import forms


class SignupForm(UserCreationForm):
    """
    Form to create a new user
    """

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        fields = ["email", "first_name", "middle_name",
                  "last_name", "date_of_birth", "gender", "photo"]


class LoginForm(AuthenticationForm):
    """
    Form to authenticate the user
    """

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        fields = "__all__"


class ChangePasswordForm(PasswordChangeForm):
    """
    Form to change password
    """

    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        fields = "__all__"


class ProfileUpdateForm(ModelForm):
    """
    Form to update the user profile
    """

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        fields = ["first_name", "middle_name", "last_name", "gender", "photo",
                  "date_of_birth", "identity_document_type", "identity_document_number"]
