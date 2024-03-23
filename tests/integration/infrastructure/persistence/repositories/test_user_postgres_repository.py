from unittest import IsolatedAsyncioTestCase

from app.domain.shared.custom_exceptions import NotFoundException
from app.domain.user.user_errors import UserErrors
from app.infrastructure.container import ApplicationContainer
from tests.assert_exception_body import assert_exception_body
from tests.factories.domain_factories import UserFactory


class TestUserPostgresRepository(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.database_session = ApplicationContainer.session_provider()
        self.repository = ApplicationContainer.user_repository()

    async def test_save_WHEN_called_THEN_persists_informed_user(self):
        await self.repository.save(self.user)
        result = await self.repository.find(self.user.id)
        self.assertEqual(self.user, result)

    async def test_find_WHEN_called_RETURNS_related_user(self):
        await self.repository.save(self.user)
        result = await self.repository.find(self.user.id)
        self.assertEqual(self.user, result)

    async def test_find_WHEN_user_not_exists_THEN_raises_not_found_exception(self):
        with self.assertRaises(NotFoundException) as ctx:
            await self.repository.find(self.user.id)

        assert_exception_body(UserErrors.not_found(), ctx)

    async def test_find_by_work_email_WHEN_called_RETURNS_related_user(self):
        await self.repository.save(self.user)
        result = await self.repository.find_by_work_email(self.user.work_email)
        self.assertEqual(self.user, result)

    async def test_find_by_work_email_WHEN_user_not_exists_THEN_raises_not_found_exception(self):
        with self.assertRaises(NotFoundException) as ctx:
            await self.repository.find_by_work_email(self.user.work_email)

        assert_exception_body(UserErrors.not_found(), ctx)

    async def test_find_by_work_email_or_enrollment_WHEN_called_with_enrollment_RETURNS_related_user(self):
        await self.repository.save(self.user)

        result = await self.repository.find_by_work_email_or_enrollment(self.user.enrollment)

        self.assertEqual(self.user, result)

    async def test_find_by_work_email_or_enrollment_WHEN_called_with_work_email_RETURNS_related_user(self):
        await self.repository.save(self.user)

        result = await self.repository.find_by_work_email_or_enrollment(self.user.work_email)

        self.assertEqual(self.user, result)

    async def test_find_by_work_email_or_enrollment_WHEN_user_not_exists_THEN_raises_not_found_exception(self):
        with self.assertRaises(NotFoundException) as ctx:
            await self.repository.find_by_work_email_or_enrollment(self.user.work_email)

        assert_exception_body(UserErrors.not_found(), ctx)
