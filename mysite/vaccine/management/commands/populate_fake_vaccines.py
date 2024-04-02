from django.core.management.base import BaseCommand
from vaccine.models import Vaccine


class Command(BaseCommand):
    help = 'Populate Fake Vaccines'

    def handle(self, *args, **kwargs):

        vaccine, created = Vaccine.objects.get_or_create(
            name="Covishield",
            defaults={
                "description": "This is a Covid-19 Vaccine.",
                "number_of_doses": "2",
                "interval": "90",
                "storage_temperature": "10",
                "minimum_age": "18",
            }
        )
        self.stdout.write(self.style.SUCCESS(
            'Successfully configured fake vaccine data'))
