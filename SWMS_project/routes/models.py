from django.db import models
from bins.models import WasteBin

# Route Model
class Route(models.Model):
    start_point = models.CharField(max_length=100)
    end_point = models.CharField(max_length=100)
    bins = models.ManyToManyField(WasteBin, related_name='routes')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Route from {self.start_point} to {self.end_point}"

