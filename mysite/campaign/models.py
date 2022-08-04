from django.db import models
from user.models import User
from vaccine.models import Vaccine
from center.models import Center
from django.db.models import F
from center.models import Storage
from django.utils.translation import gettext_lazy as _


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


class Slot(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, null=True)
    date = models.DateField(_("Date"), null=True)
    start_time = models.TimeField(_("Start Time"))
    end_time = models.TimeField(_("End Time"))
    max_capacity = models.IntegerField(_("Maximum Capacity"), default=0)
    reserved = models.IntegerField(_("Total Reserved"), default=0)

    def __str__(self):
        return str(self.date) + "|" + str(self.start_time) + " to " + str(self.end_time)

    def reserve_vaccine(slot_id):
        """
        Reserves a vaccine for given slot for a patient
        """
        slot = Slot.objects.get(id=slot_id)
        storage = Storage.objects.get(
            center=slot.campaign.center, vaccine=slot.campaign.vaccine
        )
        if slot.reserved < slot.max_capacity:
            slot.reserved = F("reserved") + 1
            storage.booked_quantity = F("booked_quantity") + 1
            slot.save()
            storage.save()
            return True
        else:
            return False
