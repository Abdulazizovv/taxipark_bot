from django.contrib import admin
from .models import ServiceCategory


class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name', 'description']
    list_filter = ['name', 'description']
    list_per_page = 10


admin.site.register(ServiceCategory, ServiceCategoryAdmin)