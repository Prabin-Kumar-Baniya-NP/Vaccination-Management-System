from django.forms import ModelForm
from medical_condition.models import Medical_Condition


class MedicalConditionCreateForm(ModelForm):
    class Meta:
        model = Medical_Condition
        fields = "__all__"


class MedicalConditionUpdateForm(ModelForm):
    class Meta:
        model = Medical_Condition
        fields = "__all__"
