from django.contrib import admin
from .models import Transaction


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('driver', 'service', 'amount', 'date', 'description', 'created_at', 'updated_at')
    list_filter = ('driver', 'date')
    search_fields = ('driver', 'description')


admin.site.register(Transaction, TransactionAdmin)