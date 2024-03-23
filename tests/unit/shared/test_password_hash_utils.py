from unittest import TestCase

from app.shared.password_hash_utils import PasswordHashUtils


class TestPasswordHashUtils(TestCase):
    def setUp(self) -> None:
        self.password_hash_utils = PasswordHashUtils()

    def test_hash_password_WHEN_called_RETURNS_hashed_password_from_plain_password(self):
        plain_password = "secure_password"

        hashed_password = self.password_hash_utils.hash_password(plain_password)

        self.assertNotEqual(plain_password, hashed_password)

    def test_hash_password_WHEN_called_with_correct_password_RETURNS_true(self):
        plain_password = "secure_password"
        hashed_password = self.password_hash_utils.hash_password(plain_password)

        result = self.password_hash_utils.verify_password(plain_password, hashed_password)

        self.assertTrue(result)

    def test_hash_password_WHEN_called_with_incorrect_password_RETURNS_false(self):
        plain_password = "secure_password"
        wrong_password = "wrong_password"
        hashed_wrong_password = self.password_hash_utils.hash_password(wrong_password)

        result = self.password_hash_utils.verify_password(plain_password, hashed_wrong_password)

        self.assertFalse(result)
