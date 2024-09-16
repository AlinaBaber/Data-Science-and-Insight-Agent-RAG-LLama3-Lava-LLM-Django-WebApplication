from django.db import models
from ..bot.models import Bot  # Import the Bot model if it's defined in a separate file
from django.contrib.auth.models import User

class Conversation(models.Model):
    id = models.BigAutoField(primary_key=True)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    users = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations')
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE)
    status = models.CharField(max_length=45, null=True)
    process_id = models.BigIntegerField(null=True)
    title = models.CharField(max_length=200, null=True)

    # # A text field to describe what the data science process is about.
    # process = models.TextField()

    def __str__(self):
        return f"Conversation {self.id}"
