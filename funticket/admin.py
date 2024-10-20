from django.contrib import admin
from funticket.models import Rate


@admin.register(Rate)
class RateAdmin(admin.ModelAdmin):
    search_fields = ['rate', 'user', 'created_at', 'modified_at', 'rate_type']
    list_display = ['rate', 'user', 'rate_type', 'created_at', 'modified_at',]
    autocomplete_fields = ['user', ]
