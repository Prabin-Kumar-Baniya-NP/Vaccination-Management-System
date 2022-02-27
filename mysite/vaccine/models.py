from django.db import models
from medical_condition.models import Medical_Condition


class Vaccine(models.Model):
    name = models.CharField("Vaccine Name", max_length=32)
    description = models.TextField("Description", max_length=1024)
    number_of_doses = models.IntegerField("Number of Doses", default=1)
    interval = models.IntegerField("Interval", default=0, help_text="Provide interval in days")
    storage_temperature = models.IntegerField("Storage Temperature", null=True, blank=True, help_text="Provide Temperature in Celcius")
    minimum_age = models.IntegerField("Minimum Age", default=0)
    ineligible_medical_condition = models.ManyToManyField(Medical_Condition, blank=True)


    def __str__(self):
        return self.name