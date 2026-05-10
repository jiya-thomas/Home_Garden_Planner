from django.db import models
from gardens.models import GardenPlot


class CareType(models.TextChoices):
    WATER = 'water', 'Watering'
    FERTILIZE = 'fertilize', 'Fertilizing'
    PRUNE = 'prune', 'Pruning'
    HARVEST = 'harvest', 'Harvesting'
    PEST_CONTROL = 'pest_control', 'Pest Control'
    WEED = 'weed', 'Weeding'
    MULCH = 'mulch', 'Mulching'
    TRANSPLANT = 'transplant', 'Transplanting'


class CareSchedule(models.Model):
    plot = models.ForeignKey(GardenPlot, on_delete=models.CASCADE, related_name='schedules')
    care_type = models.CharField(max_length=20, choices=CareType.choices)
    frequency_days = models.PositiveIntegerField(default=7, help_text='Repeat every N days')
    last_done_date = models.DateField(blank=True, null=True)
    next_due_date = models.DateField()
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['next_due_date']

    def __str__(self):
        return f"{self.get_care_type_display()} — {self.plot}"

    def mark_done(self):
        from django.utils import timezone
        from datetime import timedelta
        self.last_done_date = timezone.now().date()
        self.next_due_date = timezone.now().date() + timedelta(days=self.frequency_days)
        self.save()

    @property
    def is_overdue(self):
        from django.utils import timezone
        return self.next_due_date < timezone.now().date()

    @property
    def care_icon(self):
        icons = {
            'water': '💧',
            'fertilize': '🌿',
            'prune': '✂️',
            'harvest': '🧺',
            'pest_control': '🐛',
            'weed': '🌾',
            'mulch': '🍂',
            'transplant': '🪴',
        }
        return icons.get(self.care_type, '📋')
