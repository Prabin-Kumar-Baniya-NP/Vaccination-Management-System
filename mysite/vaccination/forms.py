from django import forms
from django.forms import ModelForm
from vaccination.models import Vaccination_Campaign, Slot, Vaccination


class CampaignCreateForm(ModelForm):
    """
    Form to create a new campaign
    """

    def __init__(self, *args, **kwargs):
        super(CampaignCreateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Vaccination_Campaign
        fields = "__all__"


class CampaignUpdateForm(ModelForm):
    """
    Form to update the campaign
    """

    def __init__(self, *args, **kwargs):
        super(CampaignUpdateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Vaccination_Campaign
        fields = "__all__"


class SlotCreateForm(ModelForm):
    """
    Form to create a new slot
    """

    def __init__(self, campaign_id, *args, **kwargs):
        super(SlotCreateForm, self).__init__(*args, **kwargs)
        self.fields["reserved"].disabled = True
        self.fields["campaign"].queryset = Vaccination_Campaign.objects.filter(
            id=campaign_id)
        self.fields["campaign"].disabled = True
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Slot
        fields = "__all__"


class SlotUpdateForm(ModelForm):
    """
    Form to update the slot
    """

    def __init__(self, campaign_id, *args, **kwargs):
        super(SlotUpdateForm, self).__init__(*args, **kwargs)
        self.fields["campaign"].queryset = Vaccination_Campaign.objects.filter(
            id=campaign_id)
        self.fields["reserved"].disabled = True
        self.fields["campaign"].disabled = True
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Slot
        fields = "__all__"


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
        labels = {
            'campaign': "Vaccine / Center Name",
            'slot': "Date / Slot"
        }
