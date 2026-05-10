from django.db import models
from django.contrib.auth.models import User

class Seed(models.Model):
    name = models.CharField(max_length=100)
    crop_type = models.CharField(max_length=50, help_text="e.g. Vegetable, Fruit, Herb")
    variety = models.CharField(max_length=100, blank=True)
    quantity_available = models.CharField(max_length=50, help_text="e.g. 500 packets, 10 kg")
    distribution_center = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.variety})" if self.variety else self.name


class Fertilizer(models.Model):
    FERTILIZER_TYPES = [
        ('Organic', 'Organic'), 
        ('Chemical', 'Chemical'), 
        ('Bio-fertilizer', 'Bio-fertilizer')
    ]
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50, choices=FERTILIZER_TYPES, default='Organic')
    quantity_available = models.CharField(max_length=50, help_text="e.g. 100 bags, 50 liters")
    description = models.TextField(blank=True)
    usage_instructions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.type})"


class FarmingTip(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='farming_tips')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
