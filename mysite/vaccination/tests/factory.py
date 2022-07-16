from datetime import datetime
import factory
from center.tests.factory import CenterFactory
from vaccine.tests.factory import VaccineFactory
from faker import Faker
from datetime import datetime, time, timedelta
from user.tests.factory import AdminUserFactory


fake = Faker()


class CampaignFactory(factory.django.DjangoModelFactory):
    center = factory.SubFactory(CenterFactory)
    vaccine = factory.SubFactory(VaccineFactory)
    start_date = fake.date_between(
        datetime.now().date(), datetime.now().date() + timedelta(days=10))
    end_date = fake.date_between(datetime.now().date(
    ) + timedelta(days=20), datetime.now().date() + timedelta(days=30))

    class Meta:
        model = "vaccination.Campaign"

    @factory.post_generation
    def agents(self, create, extracted):
        if not create:
            return

        if extracted:
            for agent in extracted:
                self.agents.add(agent)


campaign = CampaignFactory.create(
    agents=[AdminUserFactory() for i in [1, 2, 3, 4, 5]])


class SlotFactory(factory.django.DjangoModelFactory):
    campaign = campaign
    date = fake.date_between(datetime.now().date(
    ) + timedelta(days=11), datetime.now().date() + timedelta(days=19))
    start_time = factory.Iterator([
        datetime.combine(date.today(), time()) + timedelta(hours=1),
        datetime.combine(date.today(), time()) + timedelta(hours=2),
        datetime.combine(date.today(), time()) + timedelta(hours=3),
        datetime.combine(date.today(), time()) + timedelta(hours=4)
    ])
    end_time = factory.Iterator([
        datetime.combine(date.today(), time()) + timedelta(hours=2),
        datetime.combine(date.today(), time()) + timedelta(hours=3),
        datetime.combine(date.today(), time()) + timedelta(hours=4),
        datetime.combine(date.today(), time()) + timedelta(hours=5)
    ])
    max_capacity = factory.Iterator([10, 11, 12, 13, 14, 15])
    reserved = factory.Iterator([1, 2, 3, 4, 5])

    class Meta:
        model = "vaccination.Slot"


slot = SlotFactory()


class VaccinationFactory(factory.django.DjangoModelFactory):
    patient = factory.SubFactory(AdminUserFactory)
    campaign = slot.campaign
    slot = slot
    is_vaccinated = False
    updated_by = slot.campaign.agents.all()[0]
    updated_on = fake.date_time()

    class Meta:
        model = "vaccination.Vaccination"
