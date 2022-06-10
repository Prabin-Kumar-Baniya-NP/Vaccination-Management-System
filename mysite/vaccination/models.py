from django.db import models
from user.models import User
from vaccine.models import Vaccine
from center.models import Center
from django.db.models import F


class Vaccination_Campaign(models.Model):
    center = models.ForeignKey(Center, on_delete=models.CASCADE, null=True)
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE, null=True)
    start_date = models.DateField("Vaccination Campaign Start Date", null=True)
    end_date = models.DateField("Vaccination Campaign End Date", null=True)
    agents = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return str(self.vaccine.name).upper() + " | " + str(self.center.name).upper()

    def get_vaccination_campaign(center_id, vaccine_id):
        return Vaccination_Campaign.objects.filter(center=center_id, vaccine=vaccine_id)


class Slot(models.Model):
    campaign = models.ForeignKey(
        Vaccination_Campaign, on_delete=models.CASCADE, null=True)
    date = models.DateField("Date", null=True)
    start_time = models.TimeField("Start Time")
    end_time = models.TimeField("End Time")
    max_capacity = models.IntegerField("Maximum Capacity", default=0)
    reserved = models.IntegerField("Total Reserved", default=0)

    def __str__(self):
        return str(self.date) + "|" + str(self.start_time) + " to " + str(self.end_time)

    def get_available_capacity(self):
        slot = Slot.objects.get(id=self.id)
        return slot.max_capacity - slot.reserved

    def get_slots_by_campaign_id(campaign_id):
        return Slot.objects.filter(campaign=campaign_id)

    def get_available_slots(campaign_id, slot_id):
        return Slot.objects.filter(campaign=campaign_id, slot=slot_id, reserved__lt=F("max_capacity"))


class Vaccination(models.Model):
    patient = models.ForeignKey(User, related_name="patient", on_delete=models.CASCADE)
    campaign = models.ForeignKey(
        Vaccination_Campaign, on_delete=models.CASCADE)
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)
    is_vaccinated = models.BooleanField(default=False)
    updated_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE)
    updated_on = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.patient.user.get_full_name() + " | " + str(self.campaign.vaccine.name)

    def get_dose_number(patient, vaccine):
        count = 0
        vaccination = Vaccination.objects.filter(
            patient=patient, is_vaccinated=True)
        for each in vaccination.all():
            if each.campaign.vaccine == vaccine:
                count = count + 1
        return count
