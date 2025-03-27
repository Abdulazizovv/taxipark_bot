from django.contrib import admin
from .models import Driver


class DriverAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone_number', 'car_model', 'car_plate', 'tariff', 'is_deleted', 'created_at', 'updated_at')
    list_filter = ('is_deleted', 'tariff', 'created_at', 'updated_at')
    search_fields = ('full_name', 'phone_number', 'car_model', 'car_plate')
    list_per_page = 25

# django admin panelga driver modelini qo'shish
admin.site.register(Driver, DriverAdmin)
