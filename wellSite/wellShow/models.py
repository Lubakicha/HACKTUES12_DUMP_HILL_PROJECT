from django.db import models
import uuid

from django.contrib.auth.models import User

class Well(models.Model):
    well_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)   # 👈 ADD THIS
    depth = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.well_id)
    
class Record(models.Model):
    well_rec = models.ForeignKey(Well, on_delete=models.CASCADE)
    diff = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.well_rec} - {self.diff}"