from django.db import models
from user.models import Agent
from vaccine.models import Vaccine

class Center(models.Model):
    name = models.CharField("Vaccination Center Name", max_length=124)
    address = models.TextField("Address", max_length=500)
    agents = models.ManyToManyField(Agent, blank=True)


class Storage(models.Model):
    center = models.ForeignKey(Center, on_delete=models.CASCADE)
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE)
    available_quantity = models.IntegerField(default=0)
    booked_quanity = models.IntegerField(default=0)
    