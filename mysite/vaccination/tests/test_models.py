from datetime import datetime
from django.test import TestCase, Client
from vaccination.tests.factory import VaccinationFactory
from user.tests.factory import PatientUserFactory
from vaccination.models import Vaccination


class TestVaccinationView(TestCase):
    def setUp(self):
        self.c = Client()
        self.vaccination = VaccinationFactory()
        self.user = PatientUserFactory()
        self.c.login(email=self.user.email, password="abcde@12345")
        return super().setUp()

    def test_get_dose_number(self):
        self.vaccination.is_vaccinated = True
        self.vaccination.save()
        result = Vaccination.get_dose_number(
            self.vaccination.patient, self.vaccination.campaign.vaccine)
        self.assertEqual(result, 1)

    def test_documents_eligibility(self):
        checks = Vaccination.check_eligibility(
            self.vaccination.patient, self.vaccination.campaign, self.vaccination.slot)
        self.assertFalse("document" in checks.keys())

    def test_check_age_eligibility(self):
        vaccine = self.vaccination.campaign.vaccine
        vaccine.minimum_age = 0
        vaccine.save()
        checks = Vaccination.check_eligibility(
            self.vaccination.patient, self.vaccination.campaign, self.vaccination.slot)
        self.assertFalse("age" in checks.keys())

    def test_check_age_ineligibility(self):
        self.vaccination.patient.date_of_birth = datetime.now().date()
        self.vaccination.patient.save()
        checks = Vaccination.check_eligibility(
            self.vaccination.patient, self.vaccination.campaign, self.vaccination.slot)
        self.assertTrue("age" in checks.keys())

    def test_vaccine_interval_eligibility(self):
        checks = Vaccination.check_eligibility(
            self.vaccination.patient, self.vaccination.campaign, self.vaccination.slot)
        self.assertFalse("interval" in checks.keys())

    def test_vaccine_interval_ineligibility(self):
        self.vaccination.is_vaccinated = True
        self.vaccination.save()
        checks = Vaccination.check_eligibility(
            self.vaccination.patient, self.vaccination.campaign, self.vaccination.slot)
        self.assertTrue("interval" in checks.keys())
