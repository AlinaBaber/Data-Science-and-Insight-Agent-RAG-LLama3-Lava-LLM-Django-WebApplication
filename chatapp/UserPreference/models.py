from django.db import models
from django.contrib.auth.models import User

class UserPreference(models.Model):
    id = models.BigAutoField(primary_key=True)
    preference_key = models.IntegerField(null=True)
    preference_value = models.TextField(null=True)
    created_at = models.DateTimeField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='preferences')

    def __str__(self):
        return f"UserPreference {self.id}"
