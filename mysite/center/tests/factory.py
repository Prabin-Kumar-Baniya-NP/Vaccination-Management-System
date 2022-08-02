import factory
from vaccine.tests.factory import VaccineFactory
from faker import Faker

fake = Faker()


class CenterFactory(factory.django.DjangoModelFactory):
    name = factory.faker.Faker("name")
    address = fake.address()

    class Meta:
        model = "center.Center"


class StorageFactory(factory.django.DjangoModelFactory):
    center = factory.SubFactory(CenterFactory)
    vaccine = factory.SubFactory(VaccineFactory)
    total_quantity = factory.Iterator([50, 60, 70, 80])
    booked_quantity = factory.Iterator([10, 20, 30, 40])

    class Meta:
        model = "center.Storage"
