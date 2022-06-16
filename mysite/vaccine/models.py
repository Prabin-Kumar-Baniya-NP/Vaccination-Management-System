from django.db import models
from django.utils.translation import gettext_lazy as _

class Vaccine(models.Model):
    name = models.CharField(_("Vaccine Name"), max_length=32)
    description = models.TextField(_("Description"), max_length=1024)
    number_of_doses = models.IntegerField(_("Number of Doses"), default=1)
    interval = models.IntegerField(
        _("Interval"), default=0, help_text=_("Provide interval in days"))
    storage_temperature = models.IntegerField(
        _("Storage Temperature"), null=True, blank=True, help_text=_("Provide Temperature in Celcius"))
    minimum_age = models.IntegerField(_("Minimum Age"), default=0)

    def __str__(self):
        return self.name
