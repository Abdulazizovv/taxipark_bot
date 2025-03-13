from django.contrib import admin
from .models import Manager


class ManagerAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'phone_number', 'is_active', 'created_at', 'updated_at']
    list_filter = ['is_active', 'created_at', 'updated_at']
    search_fields = ['full_name', 'phone_number']
    list_per_page = 10


admin.site.register(Manager, ManagerAdmin)
