from datetime import datetime
import factory
from center.tests.factory import CenterFactory
from vaccine.tests.factory import VaccineFactory
from faker import Faker
from datetime import datetime, time, timedelta
from user.tests.factory import PatientUserFactory


fake = Faker()


class CampaignFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "vaccination.Campaign"

    center = factory.SubFactory(CenterFactory)
    vaccine = factory.SubFactory(VaccineFactory)
    start_date = fake.date_between(
        datetime.now().date(), datetime.now().date() + timedelta(days=10))
    end_date = fake.date_between(datetime.now().date(
    ) + timedelta(days=20), datetime.now().date() + timedelta(days=30))

    @factory.post_generation
    def agents(self, create, extracted):
        """
        Add agents to the objects by extracting agents from extracted.
        """
        if not create:
            return

        if extracted:
            for agent in extracted:
                self.agents.add(agent)

# campaign = CampaignFactory.create(agents=[AdminUserFactory() for i in range(5)])


class SlotFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "vaccination.Slot"

    campaign = factory.SubFactory(CampaignFactory)
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


class VaccinationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "vaccination.Vaccination"
        
    patient = factory.SubFactory(PatientUserFactory)
    campaign = factory.SubFactory(CampaignFactory)
    slot = factory.SubFactory(SlotFactory)
    is_vaccinated = False

    @factory.post_generation
    def manage_campaign_slot(self, create, extracted):
        """
        Sets the slot.campaign to object's campaign
        """
        if not create:
            return

        self.campaign = self.slot.campaign
