from django.forms import ModelForm
from center.models import Center, Storage


class CreateCenterForm(ModelForm):
    class Meta:
        model = Center
        fields = "__all__"


class UpdateCenterForm(ModelForm):
    class Meta:
        model = Center
        fields = "__all__"


class CreateStorageForm(ModelForm):
    class Meta:
        model = Storage
        fields = "__all__"


class UpdateStorageForm(ModelForm):
    class Meta:
        model = Storage
        fields = "__all__"
