from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from user.models import Patient, User, Agent
from django.forms import ModelForm


class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        fields = ["username", "first_name", "middle_name",
                  "last_name", "date_of_birth", "gender"]


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
    class Meta:
        model = User
        fields = "__all__"


class ChangePasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
    class Meta:
        model = User
        fields = "__all__"


class ProfileUpdateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
    class Meta:
        model = User
        fields = ["first_name", "middle_name", "last_name", "gender",
                  "date_of_birth", "identity_document_type", "identity_document_number"]


class AgentCreateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(AgentCreateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
    class Meta:
        model = Agent
        fields = "__all__"


class AgentUpdateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(AgentUpdateForm, self).__init__(*args, **kwargs)
        self.fields["user"].disabled = True
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
    class Meta:
        model = Agent
        fields = "__all__"


class PatientUpdateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(PatientUpdateForm, self).__init__(*args, **kwargs)
        self.fields["user"].disabled = True
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
    class Meta:
        model = Patient
        fields = "__all__"
