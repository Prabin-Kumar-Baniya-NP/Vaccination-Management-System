from django.db import models
from user.models import Agent
from user.models import Patient
from vaccine.models import Vaccine
from center.models import Center
from django.db.models import F


class Vaccination_Campaign(models.Model):
    center = models.ForeignKey(Center, on_delete=models.CASCADE, null=True)
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE, null=True)
    start_date = models.DateField("Vaccination Campaign Start Date", null=True)
    end_date = models.DateField("Vaccination Campaign End Date", null=True)

    def __str__(self):
        return str(self.vaccine.name) + " | " + str(self.center.name)

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
        return str(self.campaign) + " | Slot : " + str(self.start_time) + " to " + str(self.end_time)

    def get_available_capacity(self):
        slot = Slot.objects.get(id=self.id)
        return slot.max_capacity - slot.reserved

    def get_slots_by_campaign_id(campaign_id):
        return Slot.objects.filter(campaign=campaign_id)

    def get_available_slots(campaign_id, slot_id):
        return Slot.objects.filter(campaign=campaign_id, slot=slot_id, reserved__lt=F("max_capacity"))


class Vaccination(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE)
    dose_number = models.IntegerField("Dose Number", default=1)
    center = models.ForeignKey(Center, on_delete=models.CASCADE)
    campaign = models.ForeignKey(
        Vaccination_Campaign, on_delete=models.CASCADE)
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)
    is_vaccinated = models.BooleanField(default=False)
    updated_by = models.ForeignKey(
        Agent, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.patient.user.get_full_name() + " | Dose " + str(self.dose_number) + " | " + str(self.date.date)
