from django import forms
from .models import Task
from gardens.models import GardenBed


class TaskForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['related_garden_bed'].queryset = GardenBed.objects.filter(user=user)
        self.fields['related_garden_bed'].required = False

    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'priority', 'related_garden_bed']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
