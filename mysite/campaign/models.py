from django.db import models
from django.contrib.auth import get_user_model
from vaccine.models import Vaccine
from center.models import Center
from django.db.models import F
from center.models import Storage
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Campaign(models.Model):
    center = models.ForeignKey(
        Center, on_delete=models.CASCADE, null=True, verbose_name=_("Center")
    )
    vaccine = models.ForeignKey(
        Vaccine, on_delete=models.CASCADE, null=True, verbose_name=_("Vaccine")
    )
    start_date = models.DateField(_("Start Date"), null=True)
    end_date = models.DateField(_("End Date"), null=True)
    agents = models.ManyToManyField(User, blank=True, verbose_name=_("Agents"))

    def __str__(self):
        return str(self.vaccine.name).upper() + " | " + str(self.center.name).upper()

    def save(self, *args, **kwargs):
        '''
        If vaccine storage doesn't exists on campaign creation, then create new storage
        '''
        if not Storage.objects.filter(center=self.center, vaccine=self.vaccine).exists():
            Storage.objects.create(center=self.center, vaccine=self.vaccine)
        return super().save()


class Slot(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, null=True)
    date = models.DateField(_("Date"), null=True)
    start_time = models.TimeField(_("Start Time"))
    end_time = models.TimeField(_("End Time"))
    max_capacity = models.IntegerField(_("Maximum Capacity"), default=0)
    reserved = models.IntegerField(_("Total Reserved"), default=0)

    def __str__(self):
        return str(self.date) + "|" + str(self.start_time) + " to " + str(self.end_time)

    def reserve_vaccine(campaign_id, slot_id):
        """
        Reserves a vaccine for given slot for a patient
        Updates the value in storage and slot object
        """
        slot = Slot.objects.get(id=slot_id)
        campaign = Campaign.objects.get(id=campaign_id)
        storage = Storage.objects.get(
            center=campaign.center, vaccine=campaign.vaccine)
        if slot.reserved < slot.max_capacity:
            slot.reserved = F("reserved") + 1
            storage.booked_quantity = F("booked_quantity") + 1
            slot.save()
            storage.save()
            return True
        else:
            return False
