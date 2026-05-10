from django.contrib import admin
from .models import JournalEntry


@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ['plot', 'date', 'health_status', 'height_cm']
    list_filter = ['health_status']
    search_fields = ['plot__plant__name', 'notes']
