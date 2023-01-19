from django.urls import reverse
from django.test import TestCase, Client
from user.tests.factory import UserFactory
from center.models import Center
from center.tests.factory import CenterFactory, StorageFactory
from faker import Faker


fake = Faker()


class TestCenterView(TestCase):
    def setUp(self):
        self.c = Client()
        self.user = UserFactory(is_superuser=True, is_staff=True)
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
            reverse("center:center-detail", kwargs={"pk": self.center1.id})
        )
        response2 = self.c.get(
            reverse("center:center-detail", kwargs={"pk": self.storage1.center.id})
        )
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)

    def test_get_request_on_center_delete_page(self):
        """
        Tests whether the user can view the delete center page
        """
        response = self.c.get(
            reverse("center:center-delete", kwargs={"pk": self.center2.id})
        )
        self.assertEqual(response.status_code, 200)

    def test_post_request_on_center_delete_page(self):
        """
        Tests whether the user can delete the center object
        """
        response = self.c.post(
            reverse("center:center-delete", kwargs={"pk": self.center2.id})
        )
        self.assertFalse(Center.objects.filter(id=self.center2.id).exists())
        self.assertRedirects(response, reverse("center:center-list"))

    def test_get_request_on_center_update_page(self):
        """
        Tests whether the user can view update center page
        """
        response = self.c.get(
            reverse("center:center-update", kwargs={"pk": self.center1.id})
        )
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
            reverse("center:center-update", kwargs={"pk": self.center1.id}), data
        )
        self.center1.refresh_from_db()
        self.assertEqual(self.center1.name, data["name"])
        self.assertEqual(self.center1.address, data["address"])
