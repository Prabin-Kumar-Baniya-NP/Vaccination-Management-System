from django.db import models
from user.models import User
from campaign.models import Campaign, Slot
from django.utils.translation import gettext_lazy as _


class Vaccination(models.Model):
    patient = models.ForeignKey(
        User,
        related_name="patient",
        on_delete=models.CASCADE,
        verbose_name=_("Patient"),
    )
    campaign = models.ForeignKey(
        Campaign, on_delete=models.CASCADE, verbose_name=_("Campaign")
    )
    slot = models.ForeignKey(
        Slot, on_delete=models.CASCADE, verbose_name=_("Slot"))
    is_vaccinated = models.BooleanField(
        default=False, verbose_name=_("Is Vaccinated"))
    updated_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name=_("Updated By"),
    )
    updated_on = models.DateTimeField(
        auto_now=True, null=True, verbose_name=_("Updated On")
    )

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
