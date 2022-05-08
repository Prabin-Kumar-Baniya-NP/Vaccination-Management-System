from django.forms import ModelForm
from vaccine.models import Vaccine


class VaccineCreateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(VaccineCreateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Vaccine
        fields = "__all__"


class VaccineUpdateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(VaccineUpdateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Vaccine
        fields = "__all__"
