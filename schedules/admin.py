from django.contrib import admin
from .models import CareSchedule


@admin.register(CareSchedule)
class CareScheduleAdmin(admin.ModelAdmin):
    list_display = ['plot', 'care_type', 'frequency_days', 'next_due_date', 'is_active']
    list_filter = ['care_type', 'is_active']
