from django.contrib import admin
from .models import Seed, Fertilizer, FarmingTip

@admin.register(Seed)
class SeedAdmin(admin.ModelAdmin):
    list_display = ('name', 'crop_type', 'variety', 'quantity_available', 'distribution_center')
    search_fields = ('name', 'variety', 'distribution_center')
    list_filter = ('crop_type',)

@admin.register(Fertilizer)
class FertilizerAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'quantity_available')
    search_fields = ('name',)
    list_filter = ('type',)

@admin.register(FarmingTip)
class FarmingTipAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    search_fields = ('title', 'content')
    list_filter = ('created_at',)

