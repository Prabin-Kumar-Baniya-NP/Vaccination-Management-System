from django.contrib import admin
from vaccination.models import Vaccination


class CustomVaccinationAdmin(admin.ModelAdmin):
    change_form_template = "admin/change-vaccination.html"
    list_display = ["patient", "campaign", "slot", "is_vaccinated"]
    search_fields = ["patient__email"]
    list_filter = ["is_vaccinated"]
    readonly_fields = [
        "patient",
        "campaign",
        "is_vaccinated",
        "updated_by",
        "updated_on",
        "date",
    ]
    fields = (
        ("patient"),
        ("campaign"),
        ("slot"),
        ("is_vaccinated"),
        ("date"),
        ("updated_by"),
        ("updated_on"),
    )


admin.site.register(Vaccination, CustomVaccinationAdmin)
