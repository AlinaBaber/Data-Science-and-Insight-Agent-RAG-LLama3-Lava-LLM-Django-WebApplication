# conversation/forms.py
from django import forms
from .models import Conversation

class ConversationForm(forms.ModelForm):
    class Meta:
        model = Conversation
        fields = ['start_time', 'end_time', 'users', 'bot', 'status']
