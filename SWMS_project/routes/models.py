from django.db import models
from bins.models import WasteBin

# Route Model

class Route(models.Model):
    start_point = models.CharField(max_length=100)
    end_point = models.CharField(max_length=100)
    bins = models.ManyToManyField(WasteBin, related_name='routes')
    distance_km = models.FloatField(null=True, blank=True)   # store computed distance
    estimated_time_min = models.FloatField(null=True, blank=True)  # store computed time
    fuel_savings = models.FloatField(null=True, blank=True)
    co2_reduction = models.FloatField(null=True, blank=True)
    optimized_path = models.JSONField(null=True, blank=True)  # store lat/lng sequence
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Route from {self.start_point} to {self.end_point}"


