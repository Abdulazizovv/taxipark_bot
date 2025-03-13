from django.contrib import admin
from .models import BotUser


class BotUserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'phone_number', 'username', 'first_name', 'last_name', 'is_admin')
    list_filter = ('is_admin', 'created_at', 'updated_at')
    search_fields = ('phone_number', 'username', 'first_name', 'last_name')


admin.site.register(BotUser, BotUserAdmin)