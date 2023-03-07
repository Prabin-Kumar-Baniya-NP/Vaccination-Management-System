from django.urls import reverse
from django.test import TestCase, Client
from user.tests.factory import UserFactory
from campaign.models import Slot
from campaign.tests.factory import SlotFactory
from datetime import datetime
from faker import Faker

fake = Faker()


class TestSlotView(TestCase):
    def setUp(self):
        self.c = Client()
        self.user = UserFactory(is_superuser=True, is_staff=True)
        self.c.login(email=self.user.email, password="abcde@12345")
        self.slot = SlotFactory()
        return super().setUp()

    def test_user_can_access_create_slot_page(self):
        response = self.c.get(
            reverse(
                "campaign:slot-create", kwargs={"campaign_id": self.slot.campaign.id}
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_user_can_create_new_slot(self):
        payload = {
            "campaign": self.slot.campaign,
            "date": self.slot.campaign.start_date,
            "start_time": datetime.now().time(),
            "end_time": datetime.now().time().replace(hour=1),
            "max_capacity": 10,
        }
        response = self.c.post(
            reverse(
                "campaign:slot-create", kwargs={"campaign_id": self.slot.campaign.id}
            ),
            payload,
        )
        self.assertTrue(
            Slot.objects.filter(
                campaign=payload["campaign"],
                date=payload["date"],
                start_time=payload["start_time"],
                end_time=payload["end_time"],
            ).exists()
        )
        self.assertRedirects(
            response,
            reverse(
                "campaign:slot-list", kwargs={"campaign_id": self.slot.campaign.id}
            ),
        )

    def test_user_can_access_slot_update_page(self):
        response = self.c.get(
            reverse(
                "campaign:slot-update",
                kwargs={"campaign_id": self.slot.campaign.id, "pk": self.slot.id},
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_user_can_update_slot(self):
        payload = {
            "campaign": self.slot.campaign,
            "date": self.slot.campaign.start_date,
            "start_time": datetime.now().time(),
            "end_time": datetime.now().time().replace(hour=2),
            "max_capacity": 10,
        }
        response = self.c.post(
            reverse(
                "campaign:slot-update",
                kwargs={"campaign_id": self.slot.campaign.id, "pk": self.slot.id},
            ),
            payload,
        )
        self.slot.refresh_from_db()
        self.assertEqual(self.slot.end_time, payload["end_time"])

    def test_user_can_access_slot_list_page(self):
        response = self.c.get(
            reverse("campaign:slot-list", kwargs={"campaign_id": self.slot.campaign.id})
        )
        self.assertEqual(response.status_code, 200)

    def test_user_can_access_slot_detail_page(self):
        response = self.c.get(
            reverse("campaign:slot-detail", kwargs={"pk": self.slot.id})
        )
        self.assertEqual(response.status_code, 200)

    def test_user_can_access_slot_delete_page(self):
        response = self.c.get(
            reverse("campaign:slot-delete", kwargs={"pk": self.slot.id})
        )
        self.assertEqual(response.status_code, 200)

    def test_user_can_delete_slot(self):
        response = self.c.post(
            reverse("campaign:slot-delete", kwargs={"pk": self.slot.id})
        )
        self.assertFalse(Slot.objects.filter(id=self.slot.id).exists())
        self.assertRedirects(
            response,
            reverse(
                "campaign:slot-list", kwargs={"campaign_id": self.slot.campaign.id}
            ),
        )
