from django.db import models
from bins.models import WasteBin

# Notification Model
class Notification(models.Model):
    bin = models.ForeignKey('bins.WasteBin', on_delete=models.CASCADE, related_name='notifications')  # Correct the reference
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for Bin at {self.bin.location}"
