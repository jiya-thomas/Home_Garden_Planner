from django import forms
from .models import Plant


class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = [
            'name', 'scientific_name', 'category', 'description',
            'sun_requirement', 'water_frequency', 'days_to_germinate',
            'days_to_harvest', 'spacing_inches', 'companion_plants',
            'avoid_plants', 'planting_season', 'care_tips', 'image',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'care_tips': forms.Textarea(attrs={'rows': 3}),
        }
