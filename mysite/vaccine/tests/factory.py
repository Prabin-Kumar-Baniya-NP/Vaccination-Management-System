import factory
from vaccine.models import Vaccine


class VaccineFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Vaccine

    name = factory.faker.Faker("name")
    description = factory.faker.Faker("paragraph")
    number_of_doses = factory.Iterator([1, 2, 3, 4])
    interval = factory.Iterator([1, 2, 7, 30, 60, 90, 180, 360])
    storage_temperature = factory.Iterator([10, 20, 30])
    minimum_age = factory.Iterator([0, 1, 2, 3, 5, 17, 18, 19, 30, 40, 60, 70, 80])
