from django.forms import ModelForm
from vaccination.models import Vaccination_Campaign


class CampaignCreateForm(ModelForm):
    class Meta:
        model = Vaccination_Campaign
        fields = "__all__"


class CampaignUpdateForm(ModelForm):
    class Meta:
        model = Vaccination_Campaign
        fields = "__all__"