from django.db import models

class Bot(models.Model):
    id = models.AutoField(primary_key=True)
    bot_name = models.CharField(max_length=45, null=True)
    status = models.CharField(max_length=45, null=True)
    description = models.CharField(max_length=45, null=True)

    def __str__(self):
        return self.bot_name