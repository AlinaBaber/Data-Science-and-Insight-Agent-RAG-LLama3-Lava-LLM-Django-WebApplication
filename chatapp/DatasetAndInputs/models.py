from django.db import models
from ..Conversation.models import Conversation

from django.db import models
import json

class DatasetandInput(models.Model):
    id = models.AutoField(primary_key=True)
    file = models.FileField(upload_to='datasets/')
    target_variable = models.CharField(max_length=100, null=True)
    datetime_column = models.CharField(max_length=100, blank=True, null=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='data_and_input')
    problem_type = models.CharField(max_length=100, null=True)
    inputcolumns = models.TextField(null=True, blank=True)  # Use TextField to store JSON

    def save(self, *args, **kwargs):
        if isinstance(self.inputcolumns, list):
            self.inputcolumns = json.dumps(self.inputcolumns)
        super(DatasetandInput, self).save(*args, **kwargs)

    @property
    def inputcolumns_list(self):
        if self.inputcolumns:
            return json.loads(self.inputcolumns)
        return []

    def set_inputcolumns(self, columns):
        self.inputcolumns = json.dumps(columns)
        self.save()
