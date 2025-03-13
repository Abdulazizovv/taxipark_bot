from django.contrib import admin
from .models import BotUser


class BotUserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'phone_number', 'username', 'first_name', 'last_name', 'is_active', 'is_admin')
    list_filter = ('is_active', 'is_admin')
    search_fields = ('phone_number', 'username', 'first_name', 'last_name')


admin.site.register(BotUser, BotUserAdmin)