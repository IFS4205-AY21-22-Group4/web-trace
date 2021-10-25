from django.contrib.auth import get_user_model
from django.db import connection
from Staff_Accounts.models import Staff
from django.test import TestCase

# Create your tests here.
class CreateUser(TestCase):
    def test_create_user(self):
        user = get_user_model().objects.create_user(
            email="testdata@testing.com",
            password="xA12$$fdg2356!f5",
        )
        Staff.objects.create(
            user=user,
            roles="contact tracers",
            email_validated=True,
        )
        self.assertEqual(user.email, "testdata@testing.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)


class LogInTest(TestCase):
    def setUp(self) -> None:
        user = get_user_model().objects.create_user(
            email="testdata@testing.com",
            password="xA12$$fdg2356!f5",
        )
        Staff.objects.create(
            user=user,
            roles="contact tracers",
            email_validated=True,
        )

    def test_Login_Invalid_Username_Invalid_Password(self):
        self.credentials = {"email": "testuser@testuser.com", "password": "secret"}
        # send login data
        response = self.client.post("", self.credentials, follow=True)

        self.assertFalse(response.context["user"].is_authenticated)

    def test_Login_Valid_Username_Valid_Password(self):
        self.credentials = {
            "email": "testdata@testing.com",
            "password": "xA12$$fdg2356!f5",
        }
        # send login data
        response = self.client.post("", self.credentials, follow=True)

        self.assertTrue(
            response.context["user"].is_authenticated
        )  # Assert user can log in

    def test_Login_Valid_Username_Invalid_Password(self):
        self.credentials = {
            "email": "testdata@testing.com",
            "password": "xA12$$fdg2356!f6",
        }
        # send login data
        response = self.client.post("", self.credentials, follow=True)

        self.assertFalse(response.context["user"].is_authenticated)
