from django.contrib import admin
from center.models import Center, Storage


class CustomStorageAdmin(admin.ModelAdmin):
    fields = ["center", "vaccine", "total_quantity", "booked_quantity"]
    list_display = ["center", "vaccine"]
    ordering = ["center"]


class StorageInline(admin.TabularInline):
    model = Storage
    fk_name = "center"


class CustomCenterAdmin(admin.ModelAdmin):
    fields = ["name", "address"]
    list_display = ["name"]
    search_fields = ["name", "address"]
    inlines = [StorageInline]


admin.site.register(Center, CustomCenterAdmin)
admin.site.register(Storage, CustomStorageAdmin)
