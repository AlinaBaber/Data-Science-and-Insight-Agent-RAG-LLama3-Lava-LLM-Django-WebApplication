# bot/forms.py
from django import forms
from .models import BotResponse

class BotResponseForm(forms.ModelForm):
    class Meta:
        model = BotResponse
        fields = ['trigger_phrase', 'response_text']
