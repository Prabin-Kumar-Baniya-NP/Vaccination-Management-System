from django.urls import reverse
from django.test import TestCase, Client
from user.tests.factory import UserFactory
from center.models import Center, Storage
from center.tests.factory import CenterFactory, StorageFactory
from vaccine.tests.factory import VaccineFactory
from faker import Faker


fake = Faker()


class TestStorageView(TestCase):
    def setUp(self):
        self.c = Client()
        self.user = UserFactory(is_superuser=True, is_staff=True)
        self.c.login(email=self.user.email, password="abcde@12345")
        self.center1 = CenterFactory()
        self.center2 = CenterFactory()
        self.storage1 = StorageFactory()
        self.storage2 = StorageFactory()
        self.vaccine1 = VaccineFactory()
        self.vaccine2 = VaccineFactory()
        return super().setUp()

    def test_user_can_access_create_storage_page(self):
        response = self.c.get(
            reverse("center:storage-create", kwargs={"center_id": self.center1.id})
        )
        self.assertEqual(response.status_code, 200)

    def test_user_can_create_new_storage(self):
        payload = {
            "vaccine": self.vaccine1.id,
            "total_quantity": fake.random_int(),
        }
        response = self.c.post(
            reverse("center:storage-create", kwargs={"center_id": self.center1.id}),
            payload,
        )
        self.assertTrue(
            Storage.objects.filter(
                vaccine=payload["vaccine"], total_quantity=payload["total_quantity"]
            ).exists()
        )
        self.assertRedirects(
            response,
            reverse("center:storage-list", kwargs={"center_id": self.center1.id}),
        )

    def test_user_can_access_storage_update_page(self):
        response = self.c.get(
            reverse("center:storage-update", kwargs={"pk": self.storage1.id})
        )
        self.assertEqual(response.status_code, 200)

    def test_user_can_update_storage(self):
        payload = {
            "total_quantity": fake.random_int(),
        }
        response = self.c.post(
            reverse("center:storage-update", kwargs={"pk": self.storage1.id}), payload
        )
        self.storage1.refresh_from_db()
        self.assertEqual(self.storage1.total_quantity, payload["total_quantity"])
        self.assertRedirects(
            response,
            reverse(
                "center:storage-list", kwargs={"center_id": self.storage1.center.id}
            ),
        )

    def test_user_can_access_storage_list_page(self):
        response = self.c.get(
            reverse(
                "center:storage-list", kwargs={"center_id": self.storage1.center.id}
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_user_can_access_storage_detail_page(self):
        response = self.c.get(
            reverse("center:storage-detail", kwargs={"pk": self.storage1.id})
        )
        self.assertEqual(response.status_code, 200)

    def test_user_can_access_storage_delete_page(self):
        response = self.c.get(
            reverse("center:storage-delete", kwargs={"pk": self.storage1.id})
        )
        self.assertEqual(response.status_code, 200)

    def test_user_can_delete_storage(self):
        response = self.c.post(
            reverse("center:storage-delete", kwargs={"pk": self.storage1.id})
        )
        self.assertFalse(Storage.objects.filter(id=self.storage1.id).exists())
        self.assertRedirects(
            response,
            reverse(
                "center:storage-list", kwargs={"center_id": self.storage1.center.id}
            ),
        )
