from django.db import models
import uuid

# Create your models here.

class Well(models.Model):
    well_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    depth = models.FloatField() # bellow ground
    height = models.FloatField() # above ground

class Record(models.Model):
    well_rec = models.ForeignKey(Well, on_delete=models.CASCADE)
    timest = models.DateTimeField(auto_now_add=True)
    diff = models.FloatField()
