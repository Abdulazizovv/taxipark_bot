from django.contrib import admin
from .models import BotUser


class BotUserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'phone_number', 'username', 'first_name', 'last_name', 'role', 'created_at', 'updated_at')
    list_filter = ('role', 'created_at', 'updated_at')
    search_fields = ('phone_number', 'username', 'first_name', 'last_name')


admin.site.register(BotUser, BotUserAdmin)