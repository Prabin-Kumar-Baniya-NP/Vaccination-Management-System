from dataclasses import fields
from django.contrib import admin
from django.contrib.auth.models import Group
from user.models import User, Admin, Agent, Patient

class UserAdminView(admin.ModelAdmin):
    fields = (
        ("first_name", "middle_name", "last_name"),
        ("email", "date_of_birth"),
        ("gender"), 
        ("is_active"),
        ("photo"),
        ("identity_document_type", "identity_document_number"),
    )
    


admin.site.register(User, UserAdminView)
admin.site.register(Admin)
admin.site.register(Agent)
admin.site.register(Patient)
admin.site.unregister(Group)