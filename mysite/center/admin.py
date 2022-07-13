from django.contrib import admin
from center.models import Center, Storage


class StorageInline(admin.TabularInline):
    model = Storage
    fk_name = "center"
    fields = ["center", "vaccine", "total_quantity"]


class CustomCenterAdmin(admin.ModelAdmin):
    fields = ["name", "address"]
    list_display = ["name"]
    search_fields = ["name", "address"]
    inlines = [StorageInline]


admin.site.register(Center, CustomCenterAdmin)
