from django.contrib import admin
from vaccination.models import Slot, Vaccination_Campaign, Vaccination

admin.site.register(Slot)
admin.site.register(Vaccination_Campaign)
admin.site.register(Vaccination)
