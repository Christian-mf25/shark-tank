import uuid
from datetime import datetime, timedelta

from django.test import TestCase
from ideas.models import Idea
from users.models import User


class IdeasModel(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.username = "kenzinho"
        cls.email = "kenzinho@mail.com"
        cls.password = "1234"
        cls.phone = "(99)99999-9999"
        cls.is_superuser = False
        cls.is_inv = False
        cls.user_obj = User.objects.create_user(
            username=cls.username,
            email=cls.email,
            password=cls.password,
            phone=cls.phone,
            is_superuser=cls.is_superuser,
            is_inv=cls.is_inv,
        )

        cls.name = "mecanica"
        cls.description = "description"
        cls.value = 10000
        cls.user_idea = Idea.objects.create(
            name=cls.name,
            description=cls.description,
            value=cls.value,
            deadline=datetime.now().date() + timedelta(days=1),
            user_id=cls.user_obj.uuid,
        )

    def test_fields(self):
        self.assertIsInstance(self.user_idea.id, uuid.UUID)

        self.assertIsInstance(self.user_idea.name, str)
        self.assertEqual(self.user_idea.name, self.name)

        self.assertIsInstance(self.user_idea.description, str)
        self.assertEqual(self.user_idea.description, self.description)

        self.assertIsInstance(self.user_idea.value, int)
        self.assertEqual(self.user_idea.value, self.value)

        self.assertIsInstance(self.user_idea.amount_collected, int)
        self.assertEqual(self.user_idea.amount_collected, 0)

        self.assertIsInstance(self.user_idea.finished, bool)
        self.assertEqual(self.user_idea.finished, False)

        self.assertEqual(self.user_idea.deadline, datetime.now().date() + timedelta(days=1))

        self.assertIsInstance(self.user_idea.is_activated, bool)
        self.assertEqual(self.user_idea.is_activated, True)

        self.assertIsInstance(self.user_idea.user_id, uuid.UUID)
        self.assertEqual(self.user_idea.user_id, self.user_obj.uuid)
