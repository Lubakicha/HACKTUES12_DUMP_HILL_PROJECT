from django.db import models
import uuid

from django.contrib.auth.models import User

class Well(models.Model):
    device_id = models.CharField(
        max_length=5,
        unique=True
    )
    well_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    depth = models.FloatField()
    radius = models.FloatField()  # ✅ NEW FIELD
    created_at = models.DateTimeField(auto_now_add=True)
    critical_level = models.FloatField(null=True, blank=True)
    alert_sent = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.well_id)
    
class Record(models.Model):
    well_rec = models.ForeignKey(Well, on_delete=models.CASCADE)
    diff = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.well_rec} - {self.diff}"

class Event(models.Model):
    EVENT_TYPES = [
        ('error', 'Error'),
        ('warning', 'Warning'),
        ('info', 'Info'),
    ]

    event_type = models.CharField(max_length=10, choices=EVENT_TYPES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    related_well = models.ForeignKey(
        Well,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    # ✅ FIXED
    device_id_value = models.CharField(max_length=5, null=True, blank=True)

    resolved = models.BooleanField(default=False)