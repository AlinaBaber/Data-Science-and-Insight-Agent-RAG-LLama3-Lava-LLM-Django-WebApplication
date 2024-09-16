# bot/forms.py
from django import forms
from .models import KeywordIntent

class KeywordIntentForm(forms.ModelForm):
    class Meta:
        model = KeywordIntent
        fields = ['keyword', 'intent']  # Adjust fields as per your model
