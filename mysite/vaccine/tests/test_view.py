from django.test import TestCase, Client
from vaccine.tests.factory import VaccineFactory
from vaccine.models import Vaccine
from user.tests.factory import UserFactory
from django.urls import reverse
from faker import Faker

fake = Faker()


class TestVaccineView(TestCase):
    def setUp(self):
        self.c = Client()
        self.user = UserFactory(is_superuser=True, is_staff=True)
        self.vaccine1 = VaccineFactory()
        self.vaccine2 = VaccineFactory()
        self.c.login(email=self.user.email, password="abcde@12345")
        return super().setUp()

    def test_user_can_access_create_vaccine_page(self):
        response = self.c.get(reverse("vaccine:vaccine-create"))
        self.assertEqual(response.status_code, 200)

    def test_user_can_create_new_vaccine(self):
        payload = {
            "name": fake.name(),
            "description": fake.paragraph(),
            "number_of_doses": fake.random_int(),
            "interval": fake.random_int(),
            "storage_temperature": fake.random_int(),
            "minimum_age": fake.random_int(),
        }
        response = self.c.post(reverse("vaccine:vaccine-create"), payload)
        self.assertTrue(
            Vaccine.objects.filter(
                name=payload["name"], description=payload["description"]
            ).exists()
        )
        self.assertRedirects(response, reverse("vaccine:vaccine-list"))

    def test_user_can_access_update_vaccine_page(self):
        response = self.c.get(
            reverse("vaccine:vaccine-update", kwargs={"pk": self.vaccine1.id})
        )
        self.assertEqual(response.status_code, 200)

    def test_user_can_update_vaccine(self):
        payload = {
            "name": fake.name(),
            "description": fake.paragraph(),
            "number_of_doses": fake.random_int(),
            "interval": fake.random_int(),
            "storage_temperature": fake.random_int(),
            "minimum_age": fake.random_int(),
        }
        response = self.c.post(
            reverse("vaccine:vaccine-update", kwargs={"pk": self.vaccine1.id}), payload
        )
        self.assertTrue(
            Vaccine.objects.filter(
                name=payload["name"],
                description=payload["description"],
                number_of_doses=payload["number_of_doses"],
                interval=payload["interval"],
                storage_temperature=payload["storage_temperature"],
                minimum_age=payload["minimum_age"],
            ).exists()
        )
        self.assertRedirects(response, reverse("vaccine:vaccine-list"))

    def test_user_can_access_delete_vaccine_page(self):
        response = self.c.get(
            reverse("vaccine:vaccine-delete", kwargs={"pk": self.vaccine2.id})
        )
        self.assertTrue(response.status_code, 200)

    def test_user_can_delete_vaccine(self):
        self.c.post(reverse("vaccine:vaccine-delete", kwargs={"pk": self.vaccine2.id}))
        self.assertFalse(Vaccine.objects.filter(id=self.vaccine2.id).exists())

    def test_user_can_list_vaccine(self):
        response = self.c.get(reverse("vaccine:vaccine-list"))
        self.assertEqual(response.status_code, 200)

    def test_user_can_view_vaccine_data(self):
        response = self.c.get(
            reverse("vaccine:vaccine-detail", kwargs={"pk": self.vaccine1.id})
        )
        self.assertEqual(response.status_code, 200)
