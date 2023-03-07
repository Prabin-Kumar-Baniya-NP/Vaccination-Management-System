from django.test import TestCase, Client
from vaccination.tests.factory import VaccinationFactory
from vaccination.models import Vaccination
from campaign.tests.factory import SlotFactory
from django.utils.timezone import timedelta


class TestVaccinationView(TestCase):
    def setUp(self):
        self.c = Client()
        self.vaccination = VaccinationFactory()
        self.patient = self.vaccination.patient
        self.slot = self.vaccination.slot
        self.campaign = self.slot.campaign
        self.vaccine = self.campaign.vaccine
        self.c.login(email=self.patient.email, password="abcde@12345")
        return super().setUp()

    def test_get_dose_number(self):
        self.vaccination.is_vaccinated = True
        self.vaccination.save()
        self.assertEqual(Vaccination.get_dose_number(self.patient, self.vaccine), 1)

    def test_documents_eligibility(self):
        checks = Vaccination.check_eligibility(self.patient, self.campaign, self.slot)
        self.assertFalse("document" in checks.keys())

    def test_check_age_eligibility(self):
        self.vaccine.minimum_age = 0
        self.vaccine.save()
        checks = Vaccination.check_eligibility(self.patient, self.campaign, self.slot)
        self.assertFalse("age" in checks.keys())

    def test_check_age_ineligibility(self):
        self.vaccine.minimum_age = 1000
        self.vaccine.save()
        checks = Vaccination.check_eligibility(self.patient, self.campaign, self.slot)
        self.assertTrue("age" in checks.keys())

    def test_incomplete_vaccination_case(self):
        checks = Vaccination.check_eligibility(self.patient, self.campaign, self.slot)
        self.assertTrue("incomplete_vaccination" in checks.keys())

    def test_vaccine_interval_eligibility(self):
        checks = Vaccination.check_eligibility(self.patient, self.campaign, self.slot)
        self.assertFalse("interval" in checks.keys())

    def test_vaccine_interval_ineligibility(self):
        # Get your first vaccination done
        self.vaccination.is_vaccinated = True
        # Create new slot for existing campaign
        new_slot = SlotFactory()
        new_slot.campaign = self.vaccination.campaign
        # Make the slot date 1 day ahead of previous vaccination slot
        new_slot.date = self.vaccination.slot.date + timedelta(days=1)
        # Make the vaccine interval to 2 days and number_of_doses to 2
        self.current_vaccine = self.vaccination.campaign.vaccine
        self.current_vaccine.number_of_doses = 2
        self.current_vaccine.interval = 2
        # Save the changes
        new_slot.save()
        self.vaccination.save()
        self.current_vaccine.save()
        # Check for eligibility for vaccine
        checks = Vaccination.check_eligibility(
            self.patient, self.vaccination.campaign, new_slot
        )
        self.assertTrue("interval" in checks.keys())
