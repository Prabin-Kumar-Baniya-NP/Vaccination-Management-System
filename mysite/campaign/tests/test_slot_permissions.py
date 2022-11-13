from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.auth.models import Permission
from user.tests.factory import UserFactory
from campaign.tests.factory import SlotFactory


class TestPermissionsOnSlotView(TestCase):
    def setUp(self):
        self.c = Client()
        self.slot = SlotFactory()
        self.user = UserFactory()
        self.c.login(email=self.user.email, password="abcde@12345")
        return super().setUp()

    def test_unauthorized_access_on_create_slot_view(self):
        response = self.c.get(
            reverse("campaign:slot-create", kwargs={"campaign_id": self.slot.campaign.id}))
        self.assertEqual(response.status_code, 403)

    def test_authorized_access_on_create_slot_view(self):
        self.user.user_permissions.add(
            Permission.objects.get(codename="add_slot"))
        response = self.c.get(
            reverse("campaign:slot-create", kwargs={"campaign_id": self.slot.campaign.id}))
        self.assertEqual(response.status_code, 200)

    def test_unauthorized_access_on_update_slot_view(self):
        response = self.c.get(
            reverse("campaign:slot-update", kwargs={"pk": self.slot.id, "campaign_id": self.slot.campaign.id}))
        self.assertEqual(response.status_code, 403)

    def test_authorized_access_on_update_slot_view(self):
        self.user.user_permissions.add(
            Permission.objects.get(codename="change_slot"))
        response = self.c.get(
            reverse("campaign:slot-update", kwargs={"pk": self.slot.id, "campaign_id": self.slot.campaign.id}))
        self.assertEqual(response.status_code, 200)

    def test_unauthorized_access_on_delete_slot_view(self):
        response = self.c.get(
            reverse("campaign:slot-delete", kwargs={"pk": self.slot.id}))
        self.assertEqual(response.status_code, 403)

    def test_authorized_access_on_delete_slot_view(self):
        self.user.user_permissions.add(
            Permission.objects.get(codename="delete_slot"))
        response = self.c.get(
            reverse("campaign:slot-delete", kwargs={"pk": self.slot.id}))
        self.assertEqual(response.status_code, 200)
