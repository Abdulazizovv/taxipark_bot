from django.contrib import admin
from .models import Service


class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'phone_number', 'description']
    search_fields = ['title', 'phone_number']
    list_filter = ['category']
    list_per_page = 10

# admin panelga qo'shish
admin.site.register(Service, ServiceAdmin)