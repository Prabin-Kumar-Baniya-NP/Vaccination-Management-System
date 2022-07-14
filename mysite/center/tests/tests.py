from django.urls import reverse
from django.test import TestCase, Client
from user.tests.factory import SuperUserFactory


class TestCenterView(TestCase):

    def setUp(self):
        self.c = Client()
        return super().setUp()

    def test_get_request_on_create_center_page(self):
        """
        Tests whether the user can visit center creation page
        """
        u = SuperUserFactory()
        self.c.login(email=u.email, password="abcde@12345")
        response = self.c.get(reverse("center:create-center"))
        self.assertEqual(response.status_code, 200)
