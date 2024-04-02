from django.core.management.base import BaseCommand
from user.models import User


class Command(BaseCommand):
    help = 'Creates a Fake Super User Account'

    def handle(self, *args, **kwargs):

        admin_user, created = User.objects.get_or_create(
            email="prabin@admin.com",
            defaults={
                "first_name": "Prabin",
                "middle_name": "Kumar",
                "last_name": "Baniya",
                "date_of_birth": "2001-02-14",
                "gender": "M",
                "blood_group": "O+",
                "identity_document_type": "Passport",
                "identity_document_number": "12345678",
                "is_staff": True,
                "is_superuser": True
            }
        )
        if created:
            admin_user.set_password("abcde@12345")
            admin_user.save()

        self.stdout.write(self.style.SUCCESS('Successfully configured fake super user account'))
