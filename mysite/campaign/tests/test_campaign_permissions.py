from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.auth.models import Permission
from user.tests.factory import AdminUserFactory
from campaign.tests.factory import CampaignFactory


class TestPermissionsOnCampaignView(TestCase):
    def setUp(self):
        self.c = Client()
        self.campaign = CampaignFactory()
        self.user = AdminUserFactory()
        self.c.login(email=self.user.email, password="abcde@12345")
        return super().setUp()

    def test_unauthorized_access_on_create_campaign_view(self):
        response = self.c.get(reverse("campaign:campaign-create"))
        self.assertEqual(response.status_code, 403)

    def test_authorized_access_on_create_campaign_view(self):
        self.user.user_permissions.add(
            Permission.objects.get(codename="add_campaign"))
        response = self.c.get(reverse("campaign:campaign-create"))
        self.assertEqual(response.status_code, 200)

    def test_unauthorized_access_on_update_campaign_view(self):
        response = self.c.get(
            reverse("campaign:campaign-update", kwargs={"pk": self.campaign.id}))
        self.assertEqual(response.status_code, 403)

    def test_authorized_access_on_update_campaign_view(self):
        self.user.user_permissions.add(
            Permission.objects.get(codename="change_campaign"))
        response = self.c.get(
            reverse("campaign:campaign-update", kwargs={"pk": self.campaign.id}))
        self.assertEqual(response.status_code, 200)

    def test_unauthorized_access_on_delete_campaign_view(self):
        response = self.c.get(
            reverse("campaign:campaign-delete", kwargs={"pk": self.campaign.id}))
        self.assertEqual(response.status_code, 403)

    def test_authorized_access_on_delete_campaign_view(self):
        self.user.user_permissions.add(
            Permission.objects.get(codename="delete_campaign"))
        response = self.c.get(
            reverse("campaign:campaign-delete", kwargs={"pk": self.campaign.id}))
        self.assertEqual(response.status_code, 200)
