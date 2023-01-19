from django.contrib import admin
from vaccination.models import Slot, Campaign


class SlotInline(admin.TabularInline):
    model = Slot
    readonly_fields = ["reserved"]


class CustomCampaignAdmin(admin.ModelAdmin):
    list_display = ["vaccine", "center", "start_date", "end_date"]
    ordering = ["start_date"]
    fields = (
        ("vaccine"),
        ("center"),
        ("start_date", "end_date"),
        ("agents")
    )
    search_fields = ["vaccine__name", "center__name"]
    inlines = [SlotInline]


admin.site.register(Campaign, CustomCampaignAdmin)
