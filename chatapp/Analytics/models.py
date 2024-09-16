from django.db import models
from ..Conversation.models import Conversation  # Import the Conversation model if it's defined in a separate file
from ..messages.models import Message  # Import the Message model if it's defined in a separate file
from django.contrib.auth.models import User

class Analytics(models.Model):
    id = models.BigAutoField(primary_key=True)
    event_type = models.CharField(max_length=45, null=True)
    event_timestamp = models.DateTimeField(null=True)
    metadata = models.JSONField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)

    def __str__(self):
        return f"Analytics {self.id}"
