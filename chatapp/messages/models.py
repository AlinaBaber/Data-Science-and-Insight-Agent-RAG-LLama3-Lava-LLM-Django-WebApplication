from django.db import models
from ..Conversation.models import Conversation  # Import the Conversation model if it's defined in a separate file
from django.contrib.auth.models import User

class Message(models.Model):
    id = models.BigAutoField(primary_key=True)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Message {self.id}"
