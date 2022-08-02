from django.test import TestCase, Client
from vaccine.tests.factory import VaccineFactory
from vaccine.models import Vaccine
from user.tests.factory import SuperUserFactory
from django.urls import reverse
from faker import Faker

fake = Faker()


class TestVaccineView(TestCase):

    def setUp(self):
        self.c = Client()
        self.user = SuperUserFactory()
        self.vaccine1 = VaccineFactory()
        self.vaccine2 = VaccineFactory()
        self.c.login(email=self.user.email, password="abcde@12345")
        return super().setUp()

    def test_get_request_on_create_vaccine_view(self):
        """
        Tests whether the user can see create vaccine page
        """
        response = self.c.get(reverse("vaccine:vaccine-create"))
        self.assertEqual(response.status_code, 200)

    def test_post_request_on_create_vaccine_view(self):
        """
        Tests whether the user can create new vaccine
        """
        data = {
            "name": fake.name(),
            "description": fake.paragraph(),
            "number_of_doses": fake.random_int(),
            "interval": fake.random_int(),
            "storage_temperature": fake.random_int(),
            "minimum_age": fake.random_int(),
        }
        response = self.c.post(reverse("vaccine:vaccine-create"), data)
        self.assertTrue(Vaccine.objects.filter(
            name=data["name"], description=data["description"]).exists())
        self.assertRedirects(response, reverse("vaccine:vaccine-list"))

    def test_get_request_on_update_vaccine_page(self):
        """
        Tests whether the user can see update vaccine page
        """
        response = self.c.get(
            reverse("vaccine:vaccine-update", kwargs={"pk": self.vaccine1.id}))
        self.assertEqual(response.status_code, 200)

    def test_post_request_on_update_vaccine_page(self):
        """
        Tests whether the user can update the existing vaccine
        """
        data = {
            "name": fake.name(),
            "description": fake.paragraph(),
            "number_of_doses": fake.random_int(),
            "interval": fake.random_int(),
            "storage_temperature": fake.random_int(),
            "minimum_age": fake.random_int(),
        }
        response = self.c.post(reverse("vaccine:vaccine-update",
                                       kwargs={"pk": self.vaccine1.id}), data)
        self.assertTrue(Vaccine.objects.filter(
            name=data["name"],
            description=data["description"],
            number_of_doses=data["number_of_doses"],
            interval=data["interval"],
            storage_temperature=data["storage_temperature"],
            minimum_age=data["minimum_age"]
        ).exists())
        self.assertRedirects(response, reverse("vaccine:vaccine-list"))

    def test_get_request_on_delete_vaccine_view(self):
        """
        Tests whether the user can see delete vaccine page
        """
        response = self.c.get(
            reverse("vaccine:vaccine-delete", kwargs={"pk": self.vaccine2.id}))
        self.assertTrue(response.status_code, 200)

    def test_post_request_on_delete_vaccine_view(self):
        """
        Tests whether the user can delete existing vaccine
        """
        self.c.post(
            reverse("vaccine:vaccine-delete", kwargs={"pk": self.vaccine2.id})
        )
        self.assertFalse(Vaccine.objects.filter(id=self.vaccine2.id).exists())

    def test_get_request_on_vaccine_list_view(self):
        """
        Tests whether the user can view vaccine list page
        """
        response = self.c.get(reverse("vaccine:vaccine-list"))
        self.assertEqual(response.status_code, 200)

    def test_get_request_on_vaccine_detail_view(self):
        """
        Tests whether the user can view vaccine detail page
        """
        response = self.c.get(
            reverse("vaccine:vaccine-detail", kwargs={"pk": self.vaccine1.id}))
        self.assertEqual(response.status_code, 200)
