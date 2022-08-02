from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.auth.models import Permission
from user.tests.factory import AdminUserFactory
from center.tests.factory import CenterFactory
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
