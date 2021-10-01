from Staff_Accounts.models import CustomUser
from django.test import TestCase

# Create your tests here.
class UserModels(TestCase):
    def test_create_user(self):
        User = CustomUser
        user = User.objects.create_user(
            username="Joshua",
            email="loyo0420@gmail.com",
            password="xA12$$fdg2356!f5",
            roles="contact tracers",
            email_validated=True,
        )
        self.assertEqual(user.email, "loyo0420@gmail.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)


class LogInTest(TestCase):
    def setUp(self) -> None:
        User = CustomUser
        user = User.objects.create_user(
            username="Joshua",
            email="loyo0420@gmail.com",
            password="xA12$$fdg2356!f5",
            roles="contact tracers",
            email_validated=True,
        )

    def test_Login_Invalid_Username_Invalid_Password(self):
        self.credentials = {"username": "testuser", "password": "secret"}
        # send login data
        response = self.client.post("", self.credentials, follow=True)

        # print(response.context["user"].password)
        self.assertFalse(
            response.context["user"].is_authenticated
        )  # Assert user cannot log in

    def test_Login_Valid_Username_Valid_Password(self):
        self.credentials = {"username": "Joshua", "password": "xA12$$fdg2356!f5"}
        # send login data
        response = self.client.post("", self.credentials, follow=True)

        # print(response.context["user"].password)
        self.assertTrue(
            response.context["user"].is_authenticated
        )  # Assert user cannot log in
