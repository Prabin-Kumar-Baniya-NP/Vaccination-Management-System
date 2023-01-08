from django.db import models
from django.contrib.auth import get_user_model
from campaign.models import Campaign, Slot
from datetime import date, timedelta
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

    def check_eligibility(user, campaign, slot):
        '''
        Check whether the user is eligible to take part in vaccination campaign in the choosen slot
        '''
        def calculate_age(born):
            today = date.today()
            return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

        checks = {}

        # Check identity documents is submitted
        patient = User.objects.get(id=user.id)
        if patient.identity_document_number is None:
            checks["document"] = "Identity Document Number Not submitted"

        # check age eligibility
        vaccine = campaign.vaccine
        if calculate_age(patient.date_of_birth) < vaccine.minimum_age:
            checks["age"] = f"Your age should be more than or equal to {vaccine.minimum_age} to take this vaccine."

        # check dose number
        current_dose_num = Vaccination.get_dose_number(patient, vaccine)
        required_dose_num = vaccine.number_of_doses
        if current_dose_num >= required_dose_num:
            checks["dose"] = f"You have already taken {current_dose_num} doses of this vaccine."

        # check previous vaccination completion status
        incomplete_vaccination = Vaccination.objects.filter(patient=patient, campaign=campaign, is_vaccinated=False).exists()
        if incomplete_vaccination:
            checks["incomplete_vaccination"] = f"Please complete the previous vaccination"
        
        # check interval for taking more than one dose
        if current_dose_num >= 1 and required_dose_num > 1:
            # Get the last dose date
            campaign_list = Campaign.objects.filter(vaccine=vaccine)
            last_vaccination = Vaccination.objects.filter(
                patient=patient, campaign__in=campaign_list).last()
            # Add interval to that last dose date
            eligible_date = last_vaccination.slot.date + \
                timedelta(days=vaccine.interval)
            # Check whether slot date is less than eligible date
            if slot.date < eligible_date:
                checks["interval"] = f"You need to wait till {eligible_date} to schedule this vaccination"

        return checks
