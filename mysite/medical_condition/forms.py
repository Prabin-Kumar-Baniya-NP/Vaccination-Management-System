from django.forms import ModelForm
from medical_condition.models import Medical_Condition


class MedicalConditionCreateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(MedicalConditionCreateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Medical_Condition
        fields = "__all__"


class MedicalConditionUpdateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(MedicalConditionUpdateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Medical_Condition
        fields = "__all__"
