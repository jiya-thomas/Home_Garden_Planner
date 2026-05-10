from django.contrib import admin
from .models import Plant


@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'sun_requirement', 'water_frequency', 'days_to_harvest']
    list_filter = ['category', 'sun_requirement', 'water_frequency']
    search_fields = ['name', 'scientific_name']
    readonly_fields = ['created_at', 'updated_at']
