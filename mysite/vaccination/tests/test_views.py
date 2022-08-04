from django.urls import reverse
from django.test import TestCase, Client
from user.tests.factory import PatientUserFactory
from vaccination.tests.factory import VaccinationFactory
from vaccine.tests.factory import VaccineFactory


class TestPermissionsOnVaccinationView(TestCase):
    def setUp(self):
        self.c = Client()
        self.vaccine = VaccineFactory()
        self.vaccination = VaccinationFactory()
        self.user = PatientUserFactory()
        self.c.login(email=self.user.email, password="abcde@12345")
        return super().setUp()
    
    def test_choose_vaccine_page(self):
        response = self.c.get(reverse("vaccination:choose-vaccine"))
        self.assertEqual(response.status_code, 200)
    
    def test_choose_campaign_page(self):
        response = self.c.get(reverse("vaccination:choose-campaign", kwargs={"vaccine_id": self.vaccination.campaign.vaccine.id}))
        self.assertEqual(response.status_code, 200)
    
    def test_choose_slot_page(self):
        response = self.c.get(reverse("vaccination:choose-slot", kwargs={"campaign_id": self.vaccination.campaign.id}))
        self.assertEqual(response.status_code, 200)
    
    def test_get_request_on_confirm_vaccination(self):
        response = self.c.get(reverse("vaccination:confirm-vaccination", kwargs={"campaign_id": self.vaccination.campaign.id, "slot_id": self.vaccination.slot.id}))
        self.assertEqual(response.status_code, 200)
    
