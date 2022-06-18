from django.contrib import admin
from vaccine.models import Vaccine


class CustomVaccineAdmin(admin.ModelAdmin):
    list_display = ["name", "number_of_doses", "interval", "minimum_age"]
    search_fields = ["name", "description"]


admin.site.register(Vaccine, CustomVaccineAdmin)
