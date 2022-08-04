from django.urls import reverse
from django.test import TestCase, Client
from user.tests.factory import SuperUserFactory
from campaign.models import Slot
from campaign.tests.factory import SlotFactory
from datetime import datetime
from faker import Faker

fake = Faker()


class TestSlotView(TestCase):

    def setUp(self):
        self.c = Client()
        self.user = SuperUserFactory()
        self.c.login(email=self.user.email, password="abcde@12345")
        self.slot = SlotFactory()
        return super().setUp()

    def test_get_request_on_create_slot_page(self):
        """
        Tests whether the user can visit slot creation page
        """
        response = self.c.get(
            reverse("campaign:slot-create", kwargs={"campaign_id": self.slot.campaign.id}))
        self.assertEqual(response.status_code, 200)

    def test_post_request_on_create_slot_page(self):
        """
        Tests whether the user can create a new slot
        """
        data = {
            "campaign": self.slot.campaign,
            "date": self.slot.campaign.start_date,
            "start_time": datetime.now().time(),
            "end_time": datetime.now().time().replace(hour=1),
            "max_capacity": 10,
        }
        response = self.c.post(reverse(
            "campaign:slot-create", kwargs={"campaign_id": self.slot.campaign.id}), data)
        self.assertTrue(Slot.objects.filter(
            campaign=data["campaign"], date=data["date"], start_time=data["start_time"], end_time=data["end_time"]).exists())
        self.assertRedirects(response, reverse(
            "campaign:slot-list", kwargs={"campaign_id": self.slot.campaign.id}))

    def test_get_request_on_slot_update_page(self):
        """
        Tests whether the user can view update slot page
        """
        response = self.c.get(
            reverse("campaign:slot-update", kwargs={"campaign_id": self.slot.campaign.id, "pk": self.slot.id}))
        self.assertEqual(response.status_code, 200)

    def test_post_request_on_slot_update_page(self):
        """
        Tests whether the user can update the existing slot
        """
        data = {
            "campaign": self.slot.campaign,
            "date": self.slot.campaign.start_date,
            "start_time": datetime.now().time(),
            "end_time": datetime.now().time().replace(hour=2),
            "max_capacity": 10,
        }
        response = self.c.post(
            reverse("campaign:slot-update", kwargs={"campaign_id": self.slot.campaign.id, "pk": self.slot.id}), data)
        self.slot.refresh_from_db()
        self.assertEqual(self.slot.end_time, data["end_time"])

    def test_get_request_on_slot_list_page(self):
        """
        Tests whether the user can see slot list page
        """
        response = self.c.get(
            reverse("campaign:slot-list", kwargs={"campaign_id": self.slot.campaign.id}))
        self.assertEqual(response.status_code, 200)

    def test_get_request_on_slot_detail_page(self):
        """
        Tests whether the user can see the details of each slot
        """
        response = self.c.get(
            reverse("campaign:slot-detail", kwargs={"pk": self.slot.id}))
        self.assertEqual(response.status_code, 200)

    def test_get_request_on_slot_delete_page(self):
        """
        Tests whether the user can view the delete slot page
        """
        response = self.c.get(
            reverse("campaign:slot-delete", kwargs={"pk": self.slot.id}))
        self.assertEqual(response.status_code, 200)

    def test_post_request_on_slot_delete_page(self):
        """
        Tests whether the user can delete the slot object
        """
        response = self.c.post(reverse("campaign:slot-delete",
                                       kwargs={"pk": self.slot.id}))
        self.assertFalse(Slot.objects.filter(id=self.slot.id).exists())
        self.assertRedirects(response, reverse(
            "campaign:slot-list", kwargs={"campaign_id": self.slot.campaign.id}))
