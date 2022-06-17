from django.db import models
from user.models import User
from vaccine.models import Vaccine
from center.models import Center
from django.db.models import F
from center.models import Storage
from django.utils.translation import gettext_lazy as _


class Campaign(models.Model):
    center = models.ForeignKey(
        Center, on_delete=models.CASCADE, null=True, verbose_name=_("Center"))
    vaccine = models.ForeignKey(
        Vaccine, on_delete=models.CASCADE, null=True, verbose_name=_("Vaccine"))
    start_date = models.DateField(_("Start Date"), null=True)
    end_date = models.DateField(_("End Date"), null=True)
    agents = models.ManyToManyField(User, blank=True, verbose_name=_("Agents"))

    def __str__(self):
        return str(self.vaccine.name).upper() + " | " + str(self.center.name).upper()

    def get_campaign(center_id, vaccine_id):
        """
        Returns the vaccination campaign for given center and vaccine
        """
        return Campaign.objects.filter(center=center_id, vaccine=vaccine_id)


class Slot(models.Model):
    campaign = models.ForeignKey(
        Campaign, on_delete=models.CASCADE, null=True)
    date = models.DateField(_("Date"), null=True)
    start_time = models.TimeField(_("Start Time"))
    end_time = models.TimeField(_("End Time"))
    max_capacity = models.IntegerField(_("Maximum Capacity"), default=0)
    reserved = models.IntegerField(_("Total Reserved"), default=0)

    def __str__(self):
        return str(self.date) + "|" + str(self.start_time) + " to " + str(self.end_time)

    def get_available_capacity(self):
        """
        Returns the available vaccine quantity for given slot
        """
        slot = Slot.objects.get(id=self.id)
        return slot.max_capacity - slot.reserved

    def get_slots_by_campaign_id(campaign_id):
        """
        Returns all the slot for given campaign
        """
        return Slot.objects.filter(campaign=campaign_id)

    def get_available_slots(campaign_id, slot_id):
        """
        Returns the available slot for given campaign
        """
        return Slot.objects.filter(campaign=campaign_id, slot=slot_id, reserved__lt=F("max_capacity"))

    def reserve_vaccine(slot_id):
        """
        Reserves a vaccine for given slot for a patient
        """
        slot = Slot.objects.get(id=slot_id)
        storage = Storage.objects.get(center=slot.campaign.center)
        if slot.reserved < slot.max_capacity:
            slot.reserved = F("reserved") + 1
            storage.booked_quantity = F("booked_quantity") + 1
            slot.save()
            storage.save()
            return True
        else:
            return False


class Vaccination(models.Model):
    patient = models.ForeignKey(
        User, related_name="patient", on_delete=models.CASCADE, verbose_name=_("Patient"))
    campaign = models.ForeignKey(
        Campaign, on_delete=models.CASCADE, verbose_name=_("Campaign"))
    slot = models.ForeignKey(
        Slot, on_delete=models.CASCADE, verbose_name=_("Slot"))
    is_vaccinated = models.BooleanField(
        default=False, verbose_name=_("Is Vaccinated"))
    updated_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE, verbose_name=_("Updated By"))
    updated_on = models.DateTimeField(
        auto_now=True, null=True, verbose_name=_("Updated On"))

    def __str__(self):
        return self.patient.get_full_name() + " | " + str(self.campaign.vaccine.name)

    def get_dose_number(patient, vaccine):
        """
        Returns the dose number of the patient
        """
        count = 0
        vaccination = Vaccination.objects.filter(
            patient=patient, is_vaccinated=True)
        for each in vaccination.all():
            if each.campaign.vaccine == vaccine:
                count = count + 1
        return count
