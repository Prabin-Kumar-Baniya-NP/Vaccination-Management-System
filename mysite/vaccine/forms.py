from django.forms import ModelForm
from vaccine.models import Vaccine


class VaccineCreateForm(ModelForm):
    class Meta:
        model = Vaccine
        fields = "__all__"


class VaccineUpdateForm(ModelForm):
    class Meta:
        model = Vaccine
        fields = "__all__"
