from django.contrib import admin
from .models import GardenBed, GardenPlot


class GardenPlotInline(admin.TabularInline):
    model = GardenPlot
    extra = 0
    readonly_fields = ['expected_harvest_date', 'created_at']


@admin.register(GardenBed)
class GardenBedAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'width_ft', 'length_ft', 'soil_type', 'light_condition', 'is_active']
    list_filter = ['soil_type', 'light_condition', 'is_active']
    search_fields = ['name', 'user__username']
    inlines = [GardenPlotInline]


@admin.register(GardenPlot)
class GardenPlotAdmin(admin.ModelAdmin):
    list_display = ['plant', 'bed', 'date_planted', 'status', 'quantity']
    list_filter = ['status']
    search_fields = ['plant__name', 'bed__name']
