from django.db import models


class PlantCategory(models.TextChoices):
    VEGETABLE = 'vegetable', 'Vegetable'
    HERB = 'herb', 'Herb'
    FLOWER = 'flower', 'Flower'
    FRUIT = 'fruit', 'Fruit'
    TREE = 'tree', 'Tree'
    SHRUB = 'shrub', 'Shrub'
    VINE = 'vine', 'Vine'


class SunRequirement(models.TextChoices):
    FULL_SUN = 'full_sun', 'Full Sun (6+ hrs)'
    PARTIAL_SUN = 'partial_sun', 'Partial Sun (3-6 hrs)'
    SHADE = 'shade', 'Shade (< 3 hrs)'


class WaterFrequency(models.TextChoices):
    DAILY = 'daily', 'Daily'
    EVERY_2_DAYS = 'every_2_days', 'Every 2 Days'
    TWICE_WEEKLY = 'twice_weekly', 'Twice a Week'
    WEEKLY = 'weekly', 'Weekly'
    BIWEEKLY = 'biweekly', 'Bi-Weekly'
    MONTHLY = 'monthly', 'Monthly'


class Plant(models.Model):
    name = models.CharField(max_length=100)
    scientific_name = models.CharField(max_length=150, blank=True)
    category = models.CharField(max_length=20, choices=PlantCategory.choices, default=PlantCategory.VEGETABLE)
    description = models.TextField(blank=True)
    sun_requirement = models.CharField(max_length=20, choices=SunRequirement.choices, default=SunRequirement.FULL_SUN)
    water_frequency = models.CharField(max_length=20, choices=WaterFrequency.choices, default=WaterFrequency.WEEKLY)
    days_to_germinate = models.PositiveIntegerField(default=7, help_text='Average days to germinate')
    days_to_harvest = models.PositiveIntegerField(default=60, help_text='Average days from planting to harvest')
    spacing_inches = models.PositiveIntegerField(default=12, help_text='Spacing between plants in inches')
    companion_plants = models.CharField(max_length=255, blank=True, help_text='Comma-separated companion plant names')
    avoid_plants = models.CharField(max_length=255, blank=True, help_text='Avoid planting near these')
    planting_season = models.CharField(max_length=100, blank=True, help_text='e.g. Spring, Summer, Fall')
    care_tips = models.TextField(blank=True)
    image = models.ImageField(upload_to='plants/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def category_color(self):
        colors = {
            'vegetable': '#52B788',
            'herb': '#74C69D',
            'flower': '#F4A261',
            'fruit': '#E76F51',
            'tree': '#2D6A4F',
            'shrub': '#40916C',
            'vine': '#95D5B2',
        }
        return colors.get(self.category, '#52B788')
