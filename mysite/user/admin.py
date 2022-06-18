from django.contrib import admin
from user.models import User
from django.contrib import messages
from vaccination.models import Vaccination


@admin.action(description="Mark Selected As Staff", permissions=["change"])
def make_staff(modeladmin, request, queryset):
    queryset.update(is_staff=True)
    messages.success(request, "Selected Users Made Staff")


@admin.action(description="Mark Selected As Superuser", permissions=["change"])
def make_superuser(modeladmin, request, queryset):
    queryset.update(is_superuser=True)
    messages.success(request, "Selected Users Made Superuser")


class CustomUserAdmin(admin.ModelAdmin):
    fields = (
        ("first_name", "middle_name", "last_name"),
        ("email", "is_email_verified"),
        ("date_of_birth"),
        ("gender"),
        ("identity_document_type", "identity_document_number"),
        ("photo"),
        ("is_staff", "is_superuser", "is_active"),
        ("groups"),
        ("user_permissions")
    )
    list_display = ["first_name", "middle_name",
                    "last_name", "email", "is_active"]
    list_filter = ["is_email_verified", "identity_document_type",
                   "is_staff", "is_superuser", "is_active"]
    search_fields = ["first_name", "middle_name",
                     "last_name", "email", "identity_document_number"]
    actions = [make_staff, make_superuser]


admin.site.register(User, CustomUserAdmin)
