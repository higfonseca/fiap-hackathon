from datetime import datetime, timezone

import factory
from app.domain.user.person import User
from faker import Faker
from faker.providers import internet

fake = Faker()
fake.add_provider(internet)


class UserFactory(factory.Factory):
    class Meta:
        model = User

    id = factory.Faker("uuid4")
    name = factory.Faker("name")
    work_email = "work@email.com"
    created_at = datetime.now(timezone.utc)
    updated_at = datetime.now(timezone.utc)
    deleted_at = None
