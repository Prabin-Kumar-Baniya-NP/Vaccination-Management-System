from django.urls import reverse
from django.test import TestCase, Client
from user.tests.factory import UserFactory
from campaign.models import Campaign
from campaign.tests.factory import CampaignFactory
from center.tests.factory import CenterFactory
from vaccine.tests.factory import VaccineFactory
from faker import Faker
from datetime import datetime, timedelta


fake = Faker()


class TestCampaignView(TestCase):
    def setUp(self):
        self.c = Client()
        self.user = UserFactory(is_superuser=True, is_staff=True)
        self.c.login(email=self.user.email, password="abcde@12345")
        self.campaign = CampaignFactory()
        return super().setUp()

    def test_user_can_access_create_campaign_page(self):
        response = self.c.get(reverse("campaign:campaign-create"))
        self.assertEqual(response.status_code, 200)

    def test_user_can_create_new_campaign(self):
        payload = {
            "center": CenterFactory().id,
            "vaccine": VaccineFactory().id,
            "start_date": fake.date_between(
                datetime.now().date(), datetime.now().date() + timedelta(days=10)
            ),
            "end_date": fake.date_between(
                datetime.now().date() + timedelta(days=20),
                datetime.now().date() + timedelta(days=30),
            ),
            "agents": UserFactory().id,
        }
        response = self.c.post(reverse("campaign:campaign-create"), payload)
        self.assertTrue(
            Campaign.objects.filter(
                center=payload["center"],
                vaccine=payload["vaccine"],
                start_date=payload["start_date"],
            ).exists()
        )
        self.assertRedirects(response, reverse("campaign:campaign-list"))

    def test_user_can_access_campaign_list_page(self):
        response = self.c.get(reverse("campaign:campaign-list"))
        self.assertEqual(response.status_code, 200)

    def test_user_can_access_campaign_detail_page(self):
        response = self.c.get(
            reverse("campaign:campaign-detail", kwargs={"pk": self.campaign.id})
        )
        self.assertEqual(response.status_code, 200)

    def test_user_can_access_campaign_update_page(self):
        response = self.c.get(
            reverse("campaign:campaign-update", kwargs={"pk": self.campaign.id})
        )
        self.assertEqual(response.status_code, 200)

    def test_user_can_update_campaign(self):
        payload = {
            "center": CenterFactory().id,
            "vaccine": VaccineFactory().id,
            "start_date": fake.date_between(
                datetime.now().date(), datetime.now().date() + timedelta(days=10)
            ),
            "end_date": fake.date_between(
                datetime.now().date() + timedelta(days=20),
                datetime.now().date() + timedelta(days=30),
            ),
            "agents": UserFactory().id,
        }
        response = self.c.post(
            reverse("campaign:campaign-update", kwargs={"pk": self.campaign.id}), payload
        )
        self.campaign.refresh_from_db()
        self.assertEqual(self.campaign.center.id, payload["center"])
        self.assertEqual(self.campaign.vaccine.id, payload["vaccine"])

    def test_user_can_access_campaign_delete_page(self):
        response = self.c.get(
            reverse("campaign:campaign-delete", kwargs={"pk": self.campaign.id})
        )
        self.assertEqual(response.status_code, 200)

    def test_user_can_delete_campaign(self):
        response = self.c.post(
            reverse("campaign:campaign-delete", kwargs={"pk": self.campaign.id})
        )
        self.assertFalse(Campaign.objects.filter(id=self.campaign.id).exists())
        self.assertRedirects(response, reverse("campaign:campaign-list"))
