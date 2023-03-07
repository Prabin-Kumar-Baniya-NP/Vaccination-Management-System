from django.forms import ModelForm
from campaign.models import Campaign, Slot


class CampaignForm(ModelForm):
    """
    Form to create and update campaign
    """

    def __init__(self, *args, **kwargs):
        super(CampaignForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Campaign
        fields = "__all__"


class SlotForm(ModelForm):
    """
    Form to create a new slot
    """

    def __init__(self, campaign_id, *args, **kwargs):
        super(SlotForm, self).__init__(*args, **kwargs)
        self.fields["reserved"].disabled = True
        self.fields["campaign"].queryset = Campaign.objects.filter(
            id=campaign_id)
        self.fields["campaign"].disabled = True
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Slot
        fields = "__all__"
