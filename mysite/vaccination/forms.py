from cProfile import label
from django.forms import ModelForm
from vaccination.models import Vaccination_Campaign, Slot, Vaccination


class CampaignCreateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CampaignCreateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Vaccination_Campaign
        fields = "__all__"


class CampaignUpdateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CampaignUpdateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Vaccination_Campaign
        fields = "__all__"


class SlotCreateForm(ModelForm):
    def __init__(self, campaign_id, *args, **kwargs):
        super(SlotCreateForm, self).__init__(*args, **kwargs)
        self.fields["reserved"].disabled = True
        self.fields["campaign"].queryset = Vaccination_Campaign.objects.filter(
            id=campaign_id)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Slot
        fields = "__all__"


class SlotUpdateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(SlotUpdateForm, self).__init__(*args, **kwargs)
        self.fields["reserved"].disabled = True
        self.fields["campaign"].disabled = True
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Slot
        fields = "__all__"


class VaccinationForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(VaccinationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Vaccination
        fields = ["patient", "campaign", "slot"]
        labels = {
            'campaign': "Vaccine / Center Name",
            'slot': "Date / Slot"
        }
