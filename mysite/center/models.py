from django.db import models
from django.db.models import F
from vaccine.models import Vaccine
from django.utils.translation import gettext_lazy as _


class Center(models.Model):
    name = models.CharField(_("Vaccination Center Name"), max_length=124)
    address = models.TextField(_("Address"), max_length=500)

    def __str__(self):
        return self.name


class Storage(models.Model):
    center = models.ForeignKey(
        Center, on_delete=models.CASCADE, verbose_name=_("Center")
    )
    vaccine = models.ForeignKey(
        Vaccine, on_delete=models.CASCADE, verbose_name=_("Vaccine")
    )
    total_quantity = models.IntegerField(_("Total Quantity"), default=0)
    booked_quantity = models.IntegerField(_("Booked Quantity"), default=0)

    def __str__(self):
        return self.center.name + " | " + self.vaccine.name
