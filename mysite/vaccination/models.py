from django.db import models
from django.contrib.auth import get_user_model
from campaign.models import Campaign, Slot
from vaccine.models import Vaccine
from datetime import timedelta
from django.utils.translation import gettext_lazy as _

User = get_user_model()


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
    date = models.DateField(_("Date of Vaccination"), null=True, blank=True)
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
        return Vaccination.objects.filter(
            patient=patient,
            campaign__in=Campaign.objects.filter(id=vaccine.id),
            is_vaccinated=True).count()

    def has_incomplete_vaccination(patient, vaccine):
        """
        Returns true if patient has not completed previous scheduled vaccination
        """
        return Vaccination.objects.filter(
            patient=patient,
            campaign__in=Campaign.objects.filter(vaccine=vaccine),
            is_vaccinated=False).exists()

    def is_eligible_by_interval(patient, vaccine, slot):
        # Get the date of last vaccination
        last_vaccination = Vaccination.objects.filter(
            patient=patient,
            campaign__in=Campaign.objects.filter(vaccine=vaccine),
            is_vaccinated=True).order_by("id").last()

        if last_vaccination is None:
            return True

        # Add interval to that last dose date
        eligible_date = last_vaccination.slot.date + \
            timedelta(days=vaccine.interval)

        # Check whether slot date is less than eligible date
        if eligible_date < slot.date:
            return True

        return False

    def check_eligibility(user, campaign, slot):
        '''
        Check whether the user is eligible to take part in vaccination campaign in the choosen slot
        '''
        checks = {}

        # Check identity documents is submitted
        patient = User.objects.get(id=user.id)
        if not patient.has_submitted_identity_documents():
            checks["document"] = "Identity document not submitted"

        # check age eligibility
        vaccine = campaign.vaccine
        if not Vaccine.is_eligible_by_age(patient, vaccine):
            checks["age"] = f"Your age should be more than or equal to {vaccine.minimum_age} to take this vaccine."

        # check dose number
        current_dose_num = Vaccination.get_dose_number(patient, vaccine)
        if current_dose_num >= vaccine.number_of_doses:
            checks["dose"] = f"You have already taken {current_dose_num} doses of this vaccine."

        # check previous vaccination completion status
        if Vaccination.has_incomplete_vaccination(patient, vaccine):
            checks["incomplete_vaccination"] = f"Please complete the previous vaccination"

        # check interval for taking more than one dose
        if not Vaccination.is_eligible_by_interval(patient, vaccine, slot):
            checks["interval"] = f"You do not meet vaccine interval criteria for your next vaccination."

        return checks
