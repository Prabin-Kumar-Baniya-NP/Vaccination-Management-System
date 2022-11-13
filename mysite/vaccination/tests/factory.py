import factory
from faker import Faker
from user.tests.factory import UserFactory
from campaign.tests.factory import CampaignFactory, SlotFactory

fake = Faker()


class VaccinationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "vaccination.Vaccination"

    patient = factory.SubFactory(UserFactory)
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
