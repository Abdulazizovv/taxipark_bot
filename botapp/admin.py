from django.contrib import admin
from .models import BotUser


class BotUserAdmin(admin.ModelAdmin):
    list_display = (
        "user_id",
        "full_name",
        "username",
        "employee",
        "created_at",
        "updated_at",
    )
    list_filter = ("employee",)
    search_fields = ("full_name", "username")
    list_per_page = 20
    list_select_related = ("employee",)
    readonly_fields = ("created_at", "updated_at")

    ordering = ("-created_at",)


admin.site.register(BotUser, BotUserAdmin)
