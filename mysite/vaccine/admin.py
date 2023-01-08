from django.contrib import admin
from vaccine.models import Vaccine


class CustomVaccineAdmin(admin.ModelAdmin):
    list_display = ["name", "number_of_doses", "interval", "minimum_age"]
    ordering = ["name"]
    search_fields = ["name", "description"]
    fields = (
        ("name"),
        ("description"),
        ("number_of_doses", "interval"),
        ("minimum_age", "storage_temperature"),
    )


admin.site.register(Vaccine, CustomVaccineAdmin)
