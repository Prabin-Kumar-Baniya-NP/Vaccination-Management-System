from django.core.management.base import BaseCommand
from center.models import Center, Storage
from vaccine.models import Vaccine
from campaign.models import Campaign, Slot
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Populate Fake Campaign and Slots data. Must Run after populating fake center and storage data and after creating fake superuser account'

    def handle(self, *args, **kwargs):
        center = Center.objects.filter(name="ABC Hospital").first()
        vaccine = Vaccine.objects.filter(name="Covishield").first()
        superuser = User.objects.filter(email="prabin@admin.com").first()
        # Delete all existing campaigns and slots
        Campaign.objects.all().delete()
        if vaccine and center and superuser:
            campaign_list = []
            campaign_date = timezone.now()
            for i in range(12):
                campaign_list.append(
                    Campaign(
                        center=center,
                        vaccine=vaccine,
                        start_date=campaign_date,
                        end_date=campaign_date + timedelta(days=15)
                    )
                )
                campaign_date = campaign_date + timedelta(days=16)
            Campaign.objects.bulk_create(campaign_list)
            all_campaigns = Campaign.objects.all()
            for campaign in all_campaigns:
                campaign.agents.add(superuser)
                campaign.save()
                slot_dates = []
                for i in range(10):
                    slot_dates.append(campaign.start_date + timedelta(days=i))
                for date in slot_dates:
                    Slot.objects.get_or_create(
                        campaign=campaign,
                        date=date,
                        defaults={
                            "start_time": "9:30:00",
                            "end_time": "10:30:00",
                            "max_capacity": random.randint(5, 10),
                            "reserved": random.randint(0,5)
                        }
                    )
            self.stdout.write(self.style.SUCCESS(
                'Successfully configured fake campaign and slots data'))
