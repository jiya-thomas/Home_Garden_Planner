from django import forms
from .models import GardenBed, GardenPlot


class GardenBedForm(forms.ModelForm):
    class Meta:
        model = GardenBed
        fields = ['name', 'width_ft', 'length_ft', 'soil_type', 'light_condition', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


class GardenPlotForm(forms.ModelForm):
    class Meta:
        model = GardenPlot
        fields = ['plant', 'date_planted', 'quantity', 'status', 'row', 'col', 'notes']
        widgets = {
            'date_planted': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 2}),
        }
