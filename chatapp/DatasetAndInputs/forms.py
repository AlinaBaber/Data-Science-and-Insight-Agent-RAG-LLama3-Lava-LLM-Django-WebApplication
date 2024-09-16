from django import forms
from .models import DatasetandInput

class DatasetAndInputsForm(forms.ModelForm):
    class Meta:
        model = DatasetandInput
        fields = ['conversation', 'datetime_column', 'target_variable', 'file', 'problem_type']
