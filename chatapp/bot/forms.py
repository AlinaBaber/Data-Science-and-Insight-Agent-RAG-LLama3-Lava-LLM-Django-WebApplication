# bot/forms.py
from django import forms
from .models import Bot

class BotForm(forms.ModelForm):
    class Meta:
        model = Bot
        fields = ['bot_name', 'status', 'description']  # Fields to include in the form
