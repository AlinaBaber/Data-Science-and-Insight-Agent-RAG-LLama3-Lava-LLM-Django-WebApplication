from django.db import models
from ..messages.models import Message  # Import the Message model if it's defined in a separate file

class BotResponse(models.Model):
    id = models.BigAutoField(primary_key=True)
    trigger_phrase = models.CharField(max_length=45, null=True)
    response_text = models.TextField(max_length=5000, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='bot_responses')

    def __str__(self):
        return f"BotResponse {self.id}"
