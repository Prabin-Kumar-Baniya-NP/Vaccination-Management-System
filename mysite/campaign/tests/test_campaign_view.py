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

    def test_get_request_on_create_campaign_page(self):
        """
        Tests whether the user can visit campaign creation page
        """
        response = self.c.get(reverse("campaign:campaign-create"))
        self.assertEqual(response.status_code, 200)

    def test_post_request_on_create_campaign_page(self):
        """
        Tests whether the user can create a new campaign
        """
        data = {
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
        response = self.c.post(reverse("campaign:campaign-create"), data)
        self.assertTrue(
            Campaign.objects.filter(
                center=data["center"],
                vaccine=data["vaccine"],
                start_date=data["start_date"],
            ).exists()
        )
        self.assertRedirects(response, reverse("campaign:campaign-list"))

    def test_get_request_on_campaign_list_page(self):
        """
        Tests whether the user can see campaign list page
        """
        response = self.c.get(reverse("campaign:campaign-list"))
        self.assertEqual(response.status_code, 200)

    def test_get_request_on_campaign_detail_page(self):
        """
        Tests whether the user can see the details of each campaign
        """
        response = self.c.get(
            reverse("campaign:campaign-detail", kwargs={"pk": self.campaign.id})
        )
        self.assertEqual(response.status_code, 200)

    def test_get_request_on_campaign_update_page(self):
        """
        Tests whether the user can view update campaign page
        """
        response = self.c.get(
            reverse("campaign:campaign-update", kwargs={"pk": self.campaign.id})
        )
        self.assertEqual(response.status_code, 200)

    def test_post_request_on_campaign_update_page(self):
        """
        Tests whether the user can update the existing campaign
        """
        data = {
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
            reverse("campaign:campaign-update", kwargs={"pk": self.campaign.id}), data
        )
        self.campaign.refresh_from_db()
        self.assertEqual(self.campaign.center.id, data["center"])
        self.assertEqual(self.campaign.vaccine.id, data["vaccine"])

    def test_get_request_on_campaign_delete_page(self):
        """
        Tests whether the user can view the delete campaign page
        """
        response = self.c.get(
            reverse("campaign:campaign-delete", kwargs={"pk": self.campaign.id})
        )
        self.assertEqual(response.status_code, 200)

    def test_post_request_on_campaign_delete_page(self):
        """
        Tests whether the user can delete the campaign object
        """
        response = self.c.post(
            reverse("campaign:campaign-delete", kwargs={"pk": self.campaign.id})
        )
        self.assertFalse(Campaign.objects.filter(id=self.campaign.id).exists())
        self.assertRedirects(response, reverse("campaign:campaign-list"))
