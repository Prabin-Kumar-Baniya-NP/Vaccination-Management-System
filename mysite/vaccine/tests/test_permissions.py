from django.test import TestCase, Client
from vaccine.tests.factory import VaccineFactory
from user.tests.factory import UserFactory
from django.urls import reverse
from django.contrib.auth.models import Permission
from faker import Faker

fake = Faker()


class TestPermissionOnVaccineView(TestCase):
    def setUp(self):
        self.c = Client()
        self.user = UserFactory()
        self.vaccine = VaccineFactory()
        self.c.login(email=self.user.email, password="abcde@12345")
        return super().setUp()

    def test_unauthorized_access_on_create_vaccine_view(self):
        response = self.c.get(reverse("vaccine:vaccine-create"))
        self.assertEqual(response.status_code, 403)

    def test_authorized_access_on_create_vaccine_view(self):
        self.user.user_permissions.add(Permission.objects.get(codename="add_vaccine"))
        response = self.c.get(reverse("vaccine:vaccine-create"))
        self.assertEqual(response.status_code, 200)

    def test_unauthorized_access_on_update_vaccine_view(self):
        response = self.c.get(
            reverse("vaccine:vaccine-update", kwargs={"pk": self.vaccine.id})
        )
        self.assertEqual(response.status_code, 403)

    def test_authorized_access_on_update_vaccine_view(self):
        self.user.user_permissions.add(
            Permission.objects.get(codename="change_vaccine")
        )
        response = self.c.get(
            reverse("vaccine:vaccine-update", kwargs={"pk": self.vaccine.id})
        )
        self.assertEqual(response.status_code, 200)

    def test_unauthorized_access_on_vaccine_delete_view(self):
        response = self.c.get(
            reverse("vaccine:vaccine-delete", kwargs={"pk": self.vaccine.id})
        )
        self.assertEqual(response.status_code, 403)

    def test_authorized_access_on_vaccine_delete_view(self):
        self.user.user_permissions.add(
            Permission.objects.get(codename="delete_vaccine")
        )
        response = self.c.get(
            reverse("vaccine:vaccine-delete", kwargs={"pk": self.vaccine.id})
        )
        self.assertEqual(response.status_code, 200)
