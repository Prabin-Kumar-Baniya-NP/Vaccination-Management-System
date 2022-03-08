from django.contrib import admin
from vaccination.models import Slot, VaccinationDate, Vaccination

admin.site.register(Slot)
admin.site.register(VaccinationDate)
admin.site.register(Vaccination)
