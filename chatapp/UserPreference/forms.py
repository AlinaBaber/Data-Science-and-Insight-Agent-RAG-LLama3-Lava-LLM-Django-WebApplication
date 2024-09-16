# conversation/forms.py
from django import forms
from .models import UserPreference

class UserPreferenceForm(forms.ModelForm):
    class Meta:
        model = UserPreference
        fields = ['preference_key', 'preference_value', 'user']  # Adjust fields as per your model
