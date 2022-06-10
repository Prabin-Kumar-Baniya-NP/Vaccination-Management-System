from django.contrib import admin
from user.models import User


class UserAdminView(admin.ModelAdmin):
    fields = (
        ("first_name", "middle_name", "last_name"),
        ("email", "is_email_verified"),
        ("date_of_birth", "gender"),
        ("identity_document_type", "identity_document_number"),
        ("photo", "is_active"),
        ("groups")
    )


admin.site.register(User, UserAdminView)
