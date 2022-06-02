import uuid

from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import AbstractUser
from django.test import TestCase

from users.models import User


class UsersModelTestInvUser(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.username = "kenzinho"
        cls.email = "kenzinho@mail.com"
        cls.password = "1234"
        cls.phone = "(99)99999-9999"
        cls.is_superuser = False
        cls.is_inv = True
        cls.user_obj = User.objects.create_user(
            username=cls.username,
            email=cls.email,
            password=cls.password,
            phone=cls.phone,
            is_superuser=cls.is_superuser,
            is_inv=cls.is_inv,
        )

    def test_user_fields(self):
        self.assertIsInstance(self.user_obj.username, str)
        self.assertEqual(self.user_obj.username, self.username)

        self.assertIsInstance(self.user_obj.email, str)
        self.assertEqual(self.user_obj.email, self.email)

        self.assertIsInstance(self.user_obj.password, str)
        self.assertTrue(check_password(self.password, self.user_obj.password))

        self.assertIsInstance(self.user_obj.phone, str)
        self.assertEqual(self.user_obj.phone, self.phone)

        self.assertIsInstance(self.user_obj.is_superuser, bool)
        self.assertEqual(self.user_obj.is_superuser, self.is_superuser)

        self.assertIsInstance(self.user_obj.is_inv, bool)
        self.assertEqual(self.user_obj.is_inv, self.is_inv)

        self.assertIsInstance(self.user_obj.uuid, uuid.UUID)

        self.assertIsInstance(self.user_obj, AbstractUser)


class UsersModelTestSuperuser(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.username = "kenzinho"
        cls.email = "kenzinho@mail.com"
        cls.password = "1234"
        cls.phone = "(99)99999-9999"
        cls.is_superuser = True
        cls.is_inv = False
        cls.user_obj = User.objects.create_user(
            username=cls.username,
            email=cls.email,
            password=cls.password,
            phone=cls.phone,
            is_superuser=cls.is_superuser,
            is_inv=cls.is_inv,
        )

    def test_user_fields(self):
        self.assertIsInstance(self.user_obj.username, str)
        self.assertEqual(self.user_obj.username, self.username)

        self.assertIsInstance(self.user_obj.email, str)
        self.assertEqual(self.user_obj.email, self.email)

        self.assertIsInstance(self.user_obj.password, str)
        self.assertTrue(check_password(self.password, self.user_obj.password))

        self.assertIsInstance(self.user_obj.phone, str)
        self.assertEqual(self.user_obj.phone, self.phone)

        self.assertIsInstance(self.user_obj.is_superuser, bool)
        self.assertEqual(self.user_obj.is_superuser, self.is_superuser)

        self.assertIsInstance(self.user_obj.is_inv, bool)
        self.assertEqual(self.user_obj.is_inv, self.is_inv)

        self.assertIsInstance(self.user_obj.uuid, uuid.UUID)

        self.assertIsInstance(self.user_obj, AbstractUser)
