from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls.base import reverse

User = get_user_model()

user = {
    "email": "user@gmail.com",
    "first_name": "Super",
    "last_name": "User",
    "is_superuser": True,
    "password": "abcde@12345"
}


class TestIndexView(TestCase):
    c = Client()

    def setUp(self):
        self.user1 = User.objects.create(
            email=user["email"], first_name=user["first_name"], last_name=user["last_name"], is_superuser=user["is_superuser"])
        self.user1.set_password(user["password"])
        self.user1.save()
        return super().setUp()

    def test_anonymous_user_can_access_index_page(self):
        response = self.c.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    def test_authenticated_user_can_access_index_page(self):
        self.c.login(email=user["email"], password=user["password"])
        response = self.c.get(reverse("index"))
