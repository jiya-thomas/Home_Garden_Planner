from django.db import models
from django.contrib.auth.models import User
from plants.models import Plant


class SoilType(models.TextChoices):
    LOAMY = 'loamy', 'Loamy'
    SANDY = 'sandy', 'Sandy'
    CLAY = 'clay', 'Clay'
    SILTY = 'silty', 'Silty'
    PEATY = 'peaty', 'Peaty'
    CHALKY = 'chalky', 'Chalky'
    MIXED = 'mixed', 'Mixed / Raised Bed'


class LightCondition(models.TextChoices):
    FULL_SUN = 'full_sun', 'Full Sun'
    PARTIAL_SHADE = 'partial_shade', 'Partial Shade'
    FULL_SHADE = 'full_shade', 'Full Shade'


class GardenBed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='garden_beds')
    name = models.CharField(max_length=100)
    width_ft = models.DecimalField(max_digits=5, decimal_places=1, default=4.0)
    length_ft = models.DecimalField(max_digits=5, decimal_places=1, default=8.0)
    soil_type = models.CharField(max_length=20, choices=SoilType.choices, default=SoilType.MIXED)
    light_condition = models.CharField(max_length=20, choices=LightCondition.choices, default=LightCondition.FULL_SUN)
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.user.username})"

    @property
    def total_sqft(self):
        return float(self.width_ft) * float(self.length_ft)

    @property
    def planted_count(self):
        return self.plots.count()


class GardenPlot(models.Model):
    STATUS_CHOICES = [
        ('planted', 'Planted'),
        ('sprouted', 'Sprouted'),
        ('growing', 'Growing'),
        ('flowering', 'Flowering'),
        ('ready', 'Ready to Harvest'),
        ('harvested', 'Harvested'),
        ('failed', 'Failed / Removed'),
    ]

    bed = models.ForeignKey(GardenBed, on_delete=models.CASCADE, related_name='plots')
    plant = models.ForeignKey(Plant, on_delete=models.PROTECT, related_name='garden_plots')
    date_planted = models.DateField()
    quantity = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planted')
    row = models.PositiveIntegerField(default=1)
    col = models.PositiveIntegerField(default=1)
    notes = models.TextField(blank=True)
    expected_harvest_date = models.DateField(blank=True, null=True)
    actual_harvest_date = models.DateField(blank=True, null=True)
    harvest_yield_kg = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date_planted']

    def __str__(self):
        return f"{self.plant.name} in {self.bed.name}"

    def save(self, *args, **kwargs):
        if not self.expected_harvest_date and self.date_planted and self.plant.days_to_harvest:
            from datetime import timedelta
            self.expected_harvest_date = self.date_planted + timedelta(days=self.plant.days_to_harvest)
        super().save(*args, **kwargs)

    @property
    def days_remaining(self):
        if self.expected_harvest_date:
            from django.utils import timezone
            delta = self.expected_harvest_date - timezone.now().date()
            return max(0, delta.days)
        return None
