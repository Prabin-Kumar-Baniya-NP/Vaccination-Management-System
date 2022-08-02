from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.auth.models import Permission
from user.tests.factory import AdminUserFactory
from center.tests.factory import StorageFactory
from faker import Faker


fake = Faker()


class TestPermissionsOnStorageView(TestCase):

    def setUp(self):
        self.c = Client()
        self.storage = StorageFactory()
        self.user = AdminUserFactory()
        self.c.login(email=self.user.email, password="abcde@12345")
        return super().setUp()

    def test_unauthorized_access_on_create_storage_view(self):
        response = self.c.get(
            reverse("center:storage-create", kwargs={"center_id": self.storage.center.id}))
        self.assertEqual(response.status_code, 403)

    def test_authorized_access_on_create_storage_view(self):
        self.user.user_permissions.add(
            Permission.objects.get(codename="add_storage"))
        response = self.c.get(
            reverse("center:storage-create", kwargs={"center_id": self.storage.center.id}))
        self.assertEqual(response.status_code, 200)

    def test_unauthorized_access_on_update_storage_view(self):
        response = self.c.get(
            reverse("center:storage-update", kwargs={"pk": self.storage.id}))
        self.assertEqual(response.status_code, 403)

    def test_authorized_access_on_update_storage_view(self):
        self.user.user_permissions.add(
            Permission.objects.get(codename="change_storage"))
        response = self.c.get(
            reverse("center:storage-update", kwargs={"pk": self.storage.id}))
        self.assertEqual(response.status_code, 200)

    def test_unauthorized_access_on_storage_list_view(self):
        response = self.c.get(
            reverse("center:storage-list", kwargs={"center_id": self.storage.center.id}))
        self.assertEqual(response.status_code, 403)

    def test_authorized_access_on_storage_list_view(self):
        self.user.user_permissions.add(
            Permission.objects.get(codename="view_storage"))
        response = self.c.get(
            reverse("center:storage-list", kwargs={"center_id": self.storage.center.id}))
        self.assertEqual(response.status_code, 200)

    def test_unauthorized_access_on_storage_detail_view(self):
        response = self.c.get(
            reverse("center:storage-detail", kwargs={"pk": self.storage.id}))
        self.assertEqual(response.status_code, 403)

    def test_authorized_access_on_storage_detail_view(self):
        self.user.user_permissions.add(
            Permission.objects.get(codename="view_storage"))
        response = self.c.get(
            reverse("center:storage-detail", kwargs={"pk": self.storage.id}))
        self.assertEqual(response.status_code, 200)

    def test_unauthorized_access_on_delete_storage_view(self):
        response = self.c.get(
            reverse("center:storage-delete", kwargs={"pk": self.storage.id}))
        self.assertEqual(response.status_code, 403)

    def test_authorized_access_on_delete_storage_view(self):
        self.user.user_permissions.add(
            Permission.objects.get(codename="delete_storage"))
        response = self.c.get(
            reverse("center:storage-delete", kwargs={"pk": self.storage.id}))
        self.assertEqual(response.status_code, 200)
