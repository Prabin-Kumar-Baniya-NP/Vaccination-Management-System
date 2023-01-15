from datetime import datetime
from django.urls import reverse
from django.test import TestCase, Client
from vaccination.tests.factory import VaccinationFactory
from user.tests.factory import UserFactory
from django.contrib.auth.models import Permission


class TestVaccinationView(TestCase):
    def setUp(self):
        self.c = Client()
        self.vaccination = VaccinationFactory()
        self.user = UserFactory()
        self.c.login(email=self.user.email, password="abcde@12345")
        return super().setUp()

    def test_choose_vaccine_list_page(self):
        response = self.c.get(reverse("vaccination:choose-vaccine"))
        self.assertEqual(response.status_code, 200)

    def test_choose_campaign_list_page(self):
        response = self.c.get(reverse("vaccination:choose-campaign",
                              kwargs={"vaccine_id": self.vaccination.campaign.vaccine.id}))
        self.assertEqual(response.status_code, 200)

    def test_choose_slot_list_page(self):
        response = self.c.get(reverse(
            "vaccination:choose-slot", kwargs={"campaign_id": self.vaccination.campaign.id}))
        self.assertEqual(response.status_code, 200)

    def test_get_request_on_confirm_vaccination(self):
        response = self.c.get(reverse("vaccination:confirm-vaccination", kwargs={
                              "campaign_id": self.vaccination.campaign.id, "slot_id": self.vaccination.slot.id}))
        self.assertEqual(response.status_code, 200)

    def test_post_request_on_confirm_vaccination(self):
        # Make patient eligible for vaccination
        vaccine = self.vaccination.campaign.vaccine
        vaccine.minimum_age = 0
        vaccine.interval = 0
        vaccine.number_of_doses = 10
        self.vaccination.patient.date_of_birth = datetime.now().date()
        self.vaccination.slot.date = datetime.now().date()
        # Save the Changes
        self.vaccination.campaign.vaccine.save()
        self.vaccination.patient.save()
        self.vaccination.slot.save()
        data = {
            "patient": self.vaccination.patient.id,
            "campaign": self.vaccination.campaign.id,
            "slot": self.vaccination.slot.id,
        }
        response = self.c.post(reverse("vaccination:confirm-vaccination", kwargs={
            "campaign_id": self.vaccination.campaign.id, "slot_id": self.vaccination.slot.id}), data)
        self.assertEqual(response.status_code, 200)

    def test_approve_vaccination(self):
        response1 = self.c.get(reverse(
            "vaccination:approve-vaccination", kwargs={"vaccination_id": self.vaccination.id}))
        self.assertEqual(response1.status_code, 403)
        # Grant Permissions
        self.vaccination.campaign.agents.add(self.user)
        self.user.user_permissions.add(
            Permission.objects.get(codename="change_vaccination"))
        # Save the Changes
        self.vaccination.campaign.save()
        # Make the request
        response2 = self.c.get(reverse(
            "vaccination:approve-vaccination", kwargs={"vaccination_id": self.vaccination.id}))

        self.assertEqual(response2.status_code, 302)

    def test_vaccine_certificate(self):
        # Grant Permissions
        self.vaccination.campaign.agents.add(self.user)
        self.user.user_permissions.add(
            Permission.objects.get(codename="change_vaccination"))
        # Save the Changes
        self.vaccination.campaign.save()
        # Approve the vaccination
        self.c.get(reverse(
            "vaccination:approve-vaccination", kwargs={"vaccination_id": self.vaccination.id}))
        # Make the request
        response = self.c.get(reverse(
            "vaccination:get-certificate", kwargs={"vaccination_id": self.vaccination.id}))
        self.assertEqual(response.status_code, 200)
