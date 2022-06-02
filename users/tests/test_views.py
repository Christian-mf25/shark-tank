from urllib import response

from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User


class UsersViewTest(APITestCase):
    def test_create_user(self) -> None:
        user_data = {
            "name": "username",
            "password": "1234",
            "phone": "(99)99999-9999",
            "email": "email@email.com",
            "is_inv": False,
        }
        response = self.client.post("/api/users/", user_data)

        self.assertEqual(response.status_code, 201)
        self.assertNotIn("password", response.json())

    def test_create_user_fail(self) -> None:
        user_data = {"name": "username", "password": "1234", "phone": "(99)99999-9999", "is_inv": False}
        response = self.client.post("/api/users/", user_data)

        self.assertEqual(response.status_code, 400)
        self.assertIn("email", response.json())


class LoginViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        faker = Faker()
        cls.login_data = {"email": faker.email(), "password": "".join(faker.random_letters(length=15))}
        cls.user_data = {
            "name": faker.first_name(),
            "password": cls.login_data["password"],
            "phone": "(99)99999-9999",
            "email": cls.login_data["email"],
            "is_inv": False,
        }

    def setUp(self) -> None:
        User.objects.create_user(**self.user_data)

    def test_login(self) -> None:
        response = self.client.post("/api/login/", self.login_data)

        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.json())

    def test_login_fail_invalid_credentials(self) -> None:
        response = self.client.post("/api/login/", {"email": self.login_data["email"], "password": "1234"})

        self.assertEqual(response.status_code, 401)
        self.assertDictEqual(response.json(), {"message": "Invalid password or e-mail address"})

    def test_login_fail_invalid_body(self) -> None:
        response = self.client.post("/api/login/", {"email": self.login_data["email"]})

        self.assertEqual(response.status_code, 400)
        self.assertIn("password", response.json())
