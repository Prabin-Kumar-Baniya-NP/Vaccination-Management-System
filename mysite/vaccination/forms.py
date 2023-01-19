from django import forms
from django.forms import ModelForm
from vaccination.models import Vaccination


class VaccinationForm(ModelForm):
    """
    Form to register for new vaccination
    """

    def __init__(self, *args, **kwargs):
        super(VaccinationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget = forms.HiddenInput()

    class Meta:
        model = Vaccination
        fields = ["patient", "campaign", "slot"]
        labels = {"campaign": "Vaccine / Center Name", "slot": "Date / Slot"}
