from django.test import TestCase, Client
from user.models import User
from django.urls.base import reverse
from django.contrib.staticfiles import finders
from django.contrib.auth.hashers import check_password
from django.core import mail
import re

user = {
    "email": "user@gmail.com",
    "first_name": "Super",
    "last_name": "User",
    "is_superuser": True,
    "password": "abcde@12345",
    "photo": finders.find("images/photo.png"),
}


class TestUserAuthView(TestCase):
    def setUp(self):
        self.c = Client()
        self.user1 = User.objects.create(
            email=user["email"],
            first_name=user["first_name"],
            last_name=user["last_name"],
            is_superuser=user["is_superuser"],
            photo=user["photo"],
        )
        self.user1.set_password(user["password"])
        self.user1.save()
        return super().setUp()

    def test_user_can_view_signup_page(self):
        """
        Tests whether can view signup page
        """
        response = self.c.get(reverse("accounts:signup"))
        self.assertEqual(response.status_code, 200)

    def test_user_can_signup(self):
        """
        Tests whether a new user can signup
        """
        with open(finders.find("images/photo.png"), "rb") as profile_image:
            response = self.c.post(
                reverse("accounts:signup"),
                {
                    "email": "dummyuser@gmail.com",
                    "password1": "abcde@12345",
                    "password2": "abcde@12345",
                    "first_name": "dummy",
                    "middle_name": "dummy",
                    "last_name": "user",
                    "gender": "M",
                    "date_of_birth": "2001-01-01",
                    "photo": profile_image,
                },
            )
        self.assertTrue(User.objects.filter(email="dummyuser@gmail.com").exists())
        self.assertRedirects(response, reverse("accounts:login"))

    def test_user_can_view_login_page(self):
        """
        Tests whether the user can view login page
        """
        response = self.c.get(reverse("accounts:login"))
        self.assertEqual(response.status_code, 200)

    def test_user_can_login(self):
        """
        Tests whether the user can login or not
        """
        response = self.c.post(
            reverse("accounts:login"),
            {
                "username": user["email"],
                "password": user["password"],
            },
        )
        self.assertEqual(
            int(self.c.session["_auth_user_id"]),
            User.objects.get(email=user["email"]).id,
        )
        self.assertRedirects(response, reverse("index"))

    def test_user_can_logout(self):
        """
        Tests whether the user can logout
        """
        self.c.login(email=user["email"], password=user["password"])
        self.assertEqual(
            int(self.c.session["_auth_user_id"]),
            User.objects.get(email=user["email"]).id,
        )
        response = self.c.get(reverse("accounts:logout"))
        self.assertFalse(self.c.session.has_key("_auth_user_id"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("accounts:login"))

    def test_user_can_change_password(self):
        """
        Tests whether the user can change password
        """
        self.c.login(email=user["email"], password=user["password"])
        response = self.c.post(
            reverse("accounts:change-password"),
            {
                "old_password": "abcde@12345",
                "new_password1": "mnop@12345",
                "new_password2": "mnop@12345",
            },
        )
        password = User.objects.only("password").get(email=user["email"]).password
        self.assertTrue(check_password("mnop@12345", password))
        self.assertRedirects(response, reverse("accounts:profile-view"))

    def test_user_can_view_profile_page(self):
        """
        Tests whether the user can access the profile page
        """
        self.c.login(email=user["email"], password=user["password"])
        response = self.c.get(reverse("accounts:profile-view"))
        self.assertEqual(response.status_code, 200)

    def test_user_can_view_profile_update_page(self):
        """
        Tests whether the user can access the profile update page
        """
        self.c.login(email=user["email"], password=user["password"])
        response = self.c.get(reverse("accounts:profile-update"))
        self.assertEqual(response.status_code, 200)

    def test_user_can_update_profile(self):
        """
        Tests whether the user can update the profile
        """
        self.c.login(email=user["email"], password=user["password"])
        with open(finders.find("images/photo.png"), "rb") as profile_image:
            response = self.c.post(
                reverse("accounts:profile-update"),
                {
                    "first_name": "ABC",
                    "middle_name": "MNOP",
                    "last_name": "XYZ",
                    "gender": "F",
                    "photo": profile_image,
                    "date_of_birth": "2001-02-02",
                    "identity_document_type": "Passport",
                    "identity_document_number": "123456",
                },
            )
        self.assertTrue(
            User.objects.filter(
                first_name="ABC", middle_name="MNOP", last_name="XYZ"
            ).exists()
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("accounts:profile-view"))

    def test_user_can_send_email_verification_request(self):
        """
        Tests whether the user can send email verification request
        """
        self.c.login(email=user["email"], password=user["password"])
        response = self.c.get(reverse("accounts:verify-email"))
        self.assertEqual(response.status_code, 200)

    def test_user_can_verify_email(self):
        """
        Tests whether the user can verify the email
        """
        self.c.login(email=user["email"], password=user["password"])
        self.c.get(reverse("accounts:verify-email"))
        url = re.search("(?P<url>https?://[^\s]+)", mail.outbox[0].body).group("url")
        self.c.get(url)
        self.assertTrue(User.objects.get(email=user["email"]).is_email_verified)
