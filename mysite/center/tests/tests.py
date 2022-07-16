from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.auth.models import Permission
from user.tests.factory import SuperUserFactory, AdminUserFactory
from center.models import Center, Storage
from center.tests.factory import CenterFactory, StorageFactory
from vaccine.tests.factory import VaccineFactory
from faker import Faker


fake = Faker()


class TestPermissionsOnCenterView(TestCase):
    def setUp(self):
        self.c = Client()
        self.center = CenterFactory()
        self.user = AdminUserFactory()
        self.c.login(email=self.user.email, password="abcde@12345")
        return super().setUp()

    def test_unauthorized_access_on_create_center_view(self):
        response = self.c.get(reverse("center:create-center"))
        self.assertEqual(response.status_code, 403)

    def test_authorized_access_on_create_center_view(self):
        self.user.user_permissions.add(
            Permission.objects.get(codename="add_center"))
        response = self.c.get(reverse("center:create-center"))
        self.assertEqual(response.status_code, 200)

    def test_unauthorized_access_on_update_center_view(self):
        response = self.c.get(
            reverse("center:center-update", kwargs={"pk": self.center.id}))
        self.assertEqual(response.status_code, 403)

    def test_authorized_access_on_update_center_view(self):
        self.user.user_permissions.add(
            Permission.objects.get(codename="change_center"))
        response = self.c.get(
            reverse("center:center-update", kwargs={"pk": self.center.id}))
        self.assertEqual(response.status_code, 200)

    def test_unauthorized_access_on_center_list_view(self):
        response = self.c.get(reverse("center:center-list"))
        self.assertEqual(response.status_code, 403)

    def test_authorized_access_on_center_list_view(self):
        self.user.user_permissions.add(
            Permission.objects.get(codename="view_center"))
        response = self.c.get(reverse("center:center-list"))
        self.assertEqual(response.status_code, 200)

    def test_unauthorized_access_on_center_detail_view(self):
        response = self.c.get(
            reverse("center:center-detail", kwargs={"pk": self.center.id}))
        self.assertEqual(response.status_code, 403)

    def test_authorized_access_on_center_detail_view(self):
        self.user.user_permissions.add(
            Permission.objects.get(codename="view_center"))
        response = self.c.get(
            reverse("center:center-detail", kwargs={"pk": self.center.id}))
        self.assertEqual(response.status_code, 200)

    def test_unauthorized_access_on_delete_center_view(self):
        response = self.c.get(
            reverse("center:center-delete", kwargs={"pk": self.center.id}))
        self.assertEqual(response.status_code, 403)

    def test_authorized_access_on_delete_center_view(self):
        self.user.user_permissions.add(
            Permission.objects.get(codename="delete_center"))
        response = self.c.get(
            reverse("center:center-delete", kwargs={"pk": self.center.id}))
        self.assertEqual(response.status_code, 200)


class TestCenterView(TestCase):

    def setUp(self):
        self.c = Client()
        self.user = SuperUserFactory()
        self.c.login(email=self.user.email, password="abcde@12345")
        self.center1 = CenterFactory()
        self.center2 = CenterFactory()
        self.storage1 = StorageFactory()
        return super().setUp()

    def test_get_request_on_create_center_page(self):
        """
        Tests whether the user can visit center creation page
        """
        response = self.c.get(reverse("center:create-center"))
        self.assertEqual(response.status_code, 200)

    def test_post_request_on_create_center_page(self):
        """
        Tests whether the user can create a new center
        """
        data = {
            "name": fake.name(),
            "address": fake.address(),
        }
        response = self.c.post(reverse("center:create-center"), data)
        self.assertTrue(Center.objects.filter(name=data["name"]).exists())
        self.assertRedirects(response, reverse("center:center-list"))

    def test_get_request_on_center_list_page(self):
        """
        Tests whether the user can see center list
        """
        response = self.c.get(reverse("center:center-list"))
        self.assertEqual(response.status_code, 200)

    def test_get_request_on_center_detail_page(self):
        """
        Tests whether the user can see the details of each center
        """
        response1 = self.c.get(
            reverse("center:center-detail", kwargs={"pk": self.center1.id}))
        response2 = self.c.get(
            reverse("center:center-detail", kwargs={"pk": self.storage1.center.id}))
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)

    def test_get_request_on_center_delete_page(self):
        """
        Tests whether the user can view the delete center page
        """
        response = self.c.get(
            reverse("center:center-delete", kwargs={"pk": self.center2.id}))
        self.assertEqual(response.status_code, 200)

    def test_post_request_on_center_delete_page(self):
        """
        Tests whether the user can delete the center object
        """
        response = self.c.post(reverse("center:center-delete",
                                       kwargs={"pk": self.center2.id}))
        self.assertFalse(Center.objects.filter(id=self.center2.id).exists())
        self.assertRedirects(response, reverse("center:center-list"))

    def test_get_request_on_center_update_page(self):
        """
        Tests whether the user can view update center page
        """
        response = self.c.get(
            reverse("center:center-update", kwargs={"pk": self.center1.id}))
        self.assertEqual(response.status_code, 200)

    def test_post_request_on_center_update_page(self):
        """
        Tests whether the user can update the existing center
        """
        data = {
            "name": fake.name(),
            "address": fake.address(),
        }
        response = self.c.post(
            reverse("center:center-update", kwargs={"pk": self.center1.id}), data)
        self.center1.refresh_from_db()
        self.assertEqual(self.center1.name, data["name"])
        self.assertEqual(self.center1.address, data["address"])
        self.assertRedirects(response, reverse("center:center-list"))


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
