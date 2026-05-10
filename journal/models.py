from django.db import models
from gardens.models import GardenPlot


class HealthStatus(models.TextChoices):
    EXCELLENT = 'excellent', 'Excellent 🌟'
    GOOD = 'good', 'Good ✅'
    FAIR = 'fair', 'Fair ⚠️'
    POOR = 'poor', 'Poor ❌'


class JournalEntry(models.Model):
    plot = models.ForeignKey(GardenPlot, on_delete=models.CASCADE, related_name='journal_entries')
    date = models.DateField()
    title = models.CharField(max_length=200, blank=True)
    notes = models.TextField()
    health_status = models.CharField(max_length=10, choices=HealthStatus.choices, default=HealthStatus.GOOD)
    photo = models.ImageField(upload_to='journal/', blank=True, null=True)
    height_cm = models.DecimalField(max_digits=6, decimal_places=1, blank=True, null=True, help_text='Plant height in cm')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.plot.plant.name} — {self.date}"

    @property
    def health_color(self):
        colors = {
            'excellent': '#52B788',
            'good': '#74C69D',
            'fair': '#F4A261',
            'poor': '#E76F51',
        }
        return colors.get(self.health_status, '#74C69D')
