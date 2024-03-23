from unittest import TestCase

from app.domain.user.user_logic import UserLogic
from tests.factories.domain_factories import UserFactory


class TestUserLogic(TestCase):
    def setUp(self) -> None:
        self.user = UserFactory()

    def test_create_WHEN_called_RETURNS_user_entity(self):
        result = UserLogic.create(
            id=self.user.id,
            name=self.user.name,
            work_email=self.user.work_email,
            enrollment=self.user.enrollment,
            password=self.user.password,
        )

        self.assertEqual(self.user.id, result.id)
        self.assertEqual(self.user.name, result.name)
        self.assertEqual(self.user.work_email, result.work_email)
        self.assertEqual(self.user.enrollment, result.enrollment)
        self.assertEqual(self.user.password, result.password)
