from django import forms
from .models import Seed, Fertilizer, FarmingTip

class SeedForm(forms.ModelForm):
    class Meta:
        model = Seed
        fields = ['name', 'crop_type', 'variety', 'quantity_available', 'distribution_center', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class FertilizerForm(forms.ModelForm):
    class Meta:
        model = Fertilizer
        fields = ['name', 'type', 'quantity_available', 'description', 'usage_instructions']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'usage_instructions': forms.Textarea(attrs={'rows': 3}),
        }

class FarmingTipForm(forms.ModelForm):
    class Meta:
        model = FarmingTip
        fields = ['title', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
        }
