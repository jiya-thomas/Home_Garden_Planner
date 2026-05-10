from django import forms
from .models import CareSchedule
from gardens.models import GardenPlot


class CareScheduleForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['plot'].queryset = GardenPlot.objects.filter(
            bed__user=user
        ).select_related('plant', 'bed')

    class Meta:
        model = CareSchedule
        fields = ['plot', 'care_type', 'frequency_days', 'next_due_date', 'notes']
        widgets = {
            'next_due_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 2}),
        }
