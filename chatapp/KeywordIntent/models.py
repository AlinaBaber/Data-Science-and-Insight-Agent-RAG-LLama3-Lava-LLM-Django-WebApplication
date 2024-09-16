from django.db import models
from ..bot.models import Bot  # Import the Bot model if it's defined in a separate file

class KeywordIntent(models.Model):
    id = models.BigAutoField(primary_key=True)
    keyword = models.CharField(max_length=45, null=True)
    intent = models.CharField(max_length=45, null=True)
    created_at = models.DateTimeField(null=True)
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE)

    def __str__(self):
        return f"KeywordIntent {self.id}"
