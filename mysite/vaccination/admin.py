from django.contrib import admin
from vaccination.models import Slot, Campaign, Vaccination

admin.site.register(Slot)
admin.site.register(Campaign)
admin.site.register(Vaccination)
