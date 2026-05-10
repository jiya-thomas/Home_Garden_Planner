from django.db import models
from django.contrib.auth.models import User
from gardens.models import GardenBed


class Priority(models.TextChoices):
    LOW = 'low', 'Low'
    MEDIUM = 'medium', 'Medium'
    HIGH = 'high', 'High'
    URGENT = 'urgent', 'Urgent'


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='garden_tasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(blank=True, null=True)
    priority = models.CharField(max_length=10, choices=Priority.choices, default=Priority.MEDIUM)
    related_garden_bed = models.ForeignKey(
        GardenBed, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['is_completed', 'due_date', '-priority']

    def __str__(self):
        return self.title

    def toggle_complete(self):
        from django.utils import timezone
        self.is_completed = not self.is_completed
        self.completed_at = timezone.now() if self.is_completed else None
        self.save()

    @property
    def is_overdue(self):
        from django.utils import timezone
        return not self.is_completed and self.due_date and self.due_date < timezone.now().date()

    @property
    def priority_color(self):
        colors = {
            'low': '#74C69D',
            'medium': '#F4A261',
            'high': '#E76F51',
            'urgent': '#D62828',
        }
        return colors.get(self.priority, '#74C69D')
