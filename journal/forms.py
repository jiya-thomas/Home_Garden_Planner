from django import forms
from .models import JournalEntry
from gardens.models import GardenPlot


class JournalEntryForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['plot'].queryset = GardenPlot.objects.filter(
            bed__user=user
        ).select_related('plant', 'bed')

    class Meta:
        model = JournalEntry
        fields = ['plot', 'date', 'title', 'notes', 'health_status', 'height_cm', 'photo']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 4}),
        }
