from django.core.management.base import BaseCommand
from center.models import Center, Storage
from vaccine.models import Vaccine


class Command(BaseCommand):
    help = 'Populate Fake Center and Storage. Must Run after populating fake vaccine data'

    def handle(self, *args, **kwargs):

        vaccine = Vaccine.objects.filter(name="Covishield").first()

        if vaccine:
            center, created = Center.objects.get_or_create(
                name="ABC Hospital",
                defaults={
                    "address": "Somewhere in the capital city of India.",
                }
            )
            Storage.objects.get_or_create(
                center=center,
                vaccine=vaccine,
                defaults={
                    "total_quantity": 589,
                    "booked_quantity": 12,
                }
            )
            self.stdout.write(self.style.SUCCESS(
                'Successfully configured fake center and storage data'))
