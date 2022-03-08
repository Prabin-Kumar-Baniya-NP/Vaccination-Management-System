from django.db import models
from user.models import Agent
from user.models import Patient
from vaccine.models import Vaccine
from center.models import Center

class Slot(models.Model):
    start_time = models.TimeField("Start Time")
    end_time = models.TimeField("End Time")
    max_capacity = models.IntegerField("Maximum Capacity", default=0)
    reserved = models.IntegerField("Total Reserved", default=0)

    def __str__(self):
        return "Slot " + str(self.start_time) + " - " + str(self.end_time)

class VaccinationDate(models.Model):
    date = models.DateField("Vaccination Date")
    slots = models.ManyToManyField(Slot, blank=True)

    def __str__(self):
        return self.date

class Vaccination(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE)
    dose_number = models.IntegerField("Dose Number", default=1)
    center = models.ForeignKey(Center, on_delete=models.CASCADE)
    date = models.ForeignKey(VaccinationDate, on_delete=models.CASCADE)
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)
    is_vaccinated = models.BooleanField(default=False)
    updated_by = models.ForeignKey(Agent, null=True, blank = True, on_delete=models.CASCADE)

    def __str__(self):
        return self.patient.user.get_full_name() + " | Dose " + str(self.dose_number) + " | " + str(self.date.date)
