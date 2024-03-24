from datetime import timezone, datetime

import factory
from factory import fuzzy
from faker import Faker
from faker.providers import internet

from app.domain.record.enums import RecordType
from app.domain.record.record import Record
from app.domain.user.user import User

fake = Faker()
fake.add_provider(internet)


class UserFactory(factory.Factory):
    class Meta:
        model = User

    id = factory.Faker("uuid4")
    name = factory.Faker("name")
    work_email = factory.Faker("name")
    enrollment = factory.Faker("name")
    password = factory.Faker("password")


class RecordFactory(factory.Factory):
    class Meta:
        model = Record

    class Params:
        now_utc = datetime.now(timezone.utc)

    id = factory.Faker("uuid4")
    user = factory.SubFactory(UserFactory)
    type = fuzzy.FuzzyChoice(RecordType).fuzz()
    ref_datetime = factory.LazyFunction(lambda: datetime.now(timezone.utc))
    ref_month = factory.LazyAttribute(lambda x: x.now_utc.month)
    ref_year = factory.LazyAttribute(lambda x: x.now_utc.year)
