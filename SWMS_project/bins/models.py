from django.db import models

# Waste Bin Model
class WasteBin(models.Model):
    STATUS_CHOICES = [
        ('Empty', 'Empty'),
        ('Partially Full', 'Partially Full'),
        ('Full', 'Full'),
    ]

    location = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Empty')
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Bin at {self.location} ({self.status})"