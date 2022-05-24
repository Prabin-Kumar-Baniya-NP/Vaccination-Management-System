from dataclasses import fields
from django.contrib import admin
from django.contrib.auth.models import Group
from user.models import User, Admin, Agent, Patient


class UserAdminView(admin.ModelAdmin):
    fields = (
        ("first_name", "middle_name", "last_name"),
        ("email", "is_email_verified"),
        ("date_of_birth", "gender"),
        ("identity_document_type", "identity_document_number"),
        ("photo", "is_active"),
    )


admin.site.register(User, UserAdminView)
admin.site.register(Admin)
admin.site.register(Agent)
admin.site.register(Patient)
admin.site.unregister(Group)
