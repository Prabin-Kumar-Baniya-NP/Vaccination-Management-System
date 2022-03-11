from django.db import models
from django.db.models import F
from user.models import Agent
from vaccine.models import Vaccine

class Center(models.Model):
    name = models.CharField("Vaccination Center Name", max_length=124)
    address = models.TextField("Address", max_length=500)
    agents = models.ManyToManyField(Agent, blank=True)

    def __str__(self):
        return self.name

    def get_available_vaccine_storage(self):
        return Storage.objects.filter(center = self.id, booked_quantity__lt = F("total_quantity")).only("vaccine").prefetch_related("vaccine")

class Storage(models.Model):
    center = models.ForeignKey(Center, on_delete=models.CASCADE)
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE)
    total_quantity = models.IntegerField(default=0)
    booked_quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.center.name + " | " + self.vaccine.name
    
    def get_vaccine_quantity(center_id, vaccine_id):
        storage = Storage.objects.get(center = center_id, vaccine = vaccine_id)
        return storage.total_quantity - storage.booked_quantity
    
    def allocate_vaccine(center_id, vaccine_id, quantity):
        storage = Storage.objects.prefetch_related("center", "vaccine").get(center= center_id, vaccine = vaccine_id)
        storage.update(total_quantity = F("total_quantity") + quantity)
        return storage
    
    def get_available_storage_by_vaccine(vaccine_id):
        return Storage.objects.filter(vaccine = vaccine_id, booked_quantity__lt = F("total_quantity")).prefetch_related("center")
