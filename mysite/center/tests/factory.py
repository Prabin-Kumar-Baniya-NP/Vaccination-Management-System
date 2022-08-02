import factory
from vaccine.tests.factory import VaccineFactory
from faker import Faker

fake = Faker()


class CenterFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "center.Center"

    name = factory.faker.Faker("name")
    address = fake.address()


class StorageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "center.Storage"

    center = factory.SubFactory(CenterFactory)
    vaccine = factory.SubFactory(VaccineFactory)
    total_quantity = factory.Iterator([50, 60, 70, 80])
    booked_quantity = factory.Iterator([10, 20, 30, 40])
