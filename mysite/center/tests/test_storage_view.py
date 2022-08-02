from django.urls import reverse
from django.test import TestCase, Client
from user.tests.factory import SuperUserFactory
from center.models import Center, Storage
from center.tests.factory import CenterFactory, StorageFactory
from vaccine.tests.factory import VaccineFactory
from faker import Faker


fake = Faker()


class TestStorageView(TestCase):
    def setUp(self):
        self.c = Client()
        self.user = SuperUserFactory()
        self.c.login(email=self.user.email, password="abcde@12345")
        self.center1 = CenterFactory()
        self.center2 = CenterFactory()
        self.storage1 = StorageFactory()
        self.storage2 = StorageFactory()
        self.vaccine1 = VaccineFactory()
        self.vaccine2 = VaccineFactory()
        return super().setUp()

    def test_get_request_on_create_storage_page(self):
        """
        Tests whether the user can view create storage page
        """
        response = self.c.get(
            reverse("center:storage-create", kwargs={"center_id": self.center1.id}))
        self.assertEqual(response.status_code, 200)

    def test_post_request_on_create_storage_page(self):
        data = {
            'vaccine': self.vaccine1.id,
            "total_quantity": fake.random_int(),
        }
        response = self.c.post(
            reverse("center:storage-create", kwargs={"center_id": self.center1.id}), data)
        self.assertTrue(Storage.objects.filter(
            vaccine=data["vaccine"], total_quantity=data["total_quantity"]).exists())
        self.assertRedirects(response, reverse(
            "center:storage-list", kwargs={"center_id": self.center1.id}))

    def test_get_request_on_storage_update_page(self):
        """
        Tests whether the user can view the storage update page
        """
        response = self.c.get(
            reverse("center:storage-update", kwargs={"pk": self.storage1.id}))
        self.assertEqual(response.status_code, 200)

    def test_post_request_on_storage_update_page(self):
        """
        Tests whether the user can update the storage data
        """
        data = {
            "total_quantity": fake.random_int(),
        }
        response = self.c.post(
            reverse("center:storage-update", kwargs={"pk": self.storage1.id}), data)
        self.storage1.refresh_from_db()
        self.assertEqual(self.storage1.total_quantity, data["total_quantity"])
        self.assertRedirects(response, reverse(
            "center:storage-list", kwargs={"center_id": self.storage1.center.id}))

    def test_get_request_on_storage_list_page(self):
        """
        Tests whether the user can view the storage list of given center
        """
        response = self.c.get(
            reverse("center:storage-list", kwargs={"center_id": self.storage1.center.id}))
        self.assertEqual(response.status_code, 200)

    def test_get_request_on_storage_detail_page(self):
        """
        Tests whether the user can view the storage details
        """
        response = self.c.get(
            reverse("center:storage-detail", kwargs={"pk": self.storage1.id})
        )
        self.assertEqual(response.status_code, 200)

    def test_get_request_on_storage_delete_page(self):
        """
        Tests whether the user can view delete storage page
        """
        response = self.c.get(
            reverse("center:storage-delete", kwargs={"pk": self.storage1.id})
        )
        self.assertEqual(response.status_code, 200)

    def test_post_request_on_storage_delete_page(self):
        """
        Tests whether the user can delete storage object
        """
        response = self.c.post(
            reverse("center:storage-delete", kwargs={"pk": self.storage1.id})
        )
        self.assertFalse(Storage.objects.filter(id=self.storage1.id).exists())
        self.assertRedirects(response, reverse(
            "center:storage-list", kwargs={"center_id": self.storage1.center.id}))
